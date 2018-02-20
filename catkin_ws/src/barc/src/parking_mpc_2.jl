#!/usr/bin/env julia

using RobotOS
@rosimport barc.msg: ECU,  Z_KinBkMdl
@rosimport data_service.msg: TimeData
@rosimport geometry_msgs.msg: Vector3,  PointStamped
@rosimport geometry_msgs.msg: Vector3
@rosimport ackermann_msgs.msg: AckermannDrive, AckermannDriveStamped
@rosimport nav_msgs.msg: Path, Odometry
@rosimport duckietown_msgs.msg: Twist2DStamped, LanePose

rostypegen()
using barc.msg
using data_service.msg
using geometry_msgs.msg
using ackermann_msgs.msg
using nav_msgs.msg
using JuMP
using Ipopt
using Distances
using duckietown_msgs.msg


# define model parameters
L_a     = 0.1         # distance from CoG to front axel
L_b     = 0.1         # distance from CoG to rear axel
dt      = 0.1           # time step of system
la      =0.08           # center to front wheel of trycicle model
T       = 150  # MPC horizon
dt=0.1 # Smapling time
global Getpos  = false
zmax=[10;10;100*pi]
umax=[0.6;3*dt]
n=3
m=2
# predictive horizon

l       = 0.1   #length of the car
X=[0.0;0.0;0.0]
path = Path()


function solveMPC(l,n,m,T,z0,zT,zmax,umax,dt,step)
    #T : horizon
    #z0 : intial position for every iteration
    #zT : reference   +++++++++++++++
    #n :dim of input
    #m : dim of state
    #
    mpc = Model(solver=IpoptSolver(print_level=0))
    @defVar(mpc, -zmax[i] <= z[t=1:T+1,i=1:n] <= zmax[i])
    @defVar(mpc, -umax[i] <= u[t=1:T+1,i=1:m] <= umax[i])

    # Cost
    #@setObjective(mpc, Min,
    #    sum{100*(z[1,t]+z[2,t]+z[3,t]+z[4,t])^2 + sum{u[j,t]^2,j=1:m},t=0:T})
    #@setObjective(mpc, Min,
    #sum{(z[t,1]-zT[t,1])^2+(z[t,2]-zT[t,2])^2+10e-5*(z[t,3]-zT[t,3])^2  ,t=2:T+1})
@defNLExpr(mpc, bta[i = 1:T], atan( L_a / (L_a + L_b) * tan(u[i,1]) ) )
      @setObjective(mpc, Min,
    sum{(z[T,1]-zT[1])^2+(z[T,2]-zT[2])^2+(z[T,3]-zT[3])^2,t=1:T})
    # Link state and control across the horizon
    for t = 1:T       
        @addNLConstraint(mpc, z[t+1,1] == z[t,1] + dt*u[t,2]*cos(z[t,3]))
        @addNLConstraint(mpc, z[t+1,2] == z[t,2] + dt*u[t,2]*sin(z[t,3]))
        @addNLConstraint(mpc, z[t+1,3] == z[t,3] + dt*u[t,2]/l*sin(bta[t]))
        #@addNLConstraint(mpc, z[t+1,4] == z[t,4] + dt*u[t,2])

    end
    
    # Initial conditions
    @addConstraint(mpc, z[1,:] .== z0)
    # Final state
    #@addConstraint(mpc, z[:,T] .== zT)
    # Solve the NLP
    solve(mpc)
    # Return the control plan
    step = step +1
    return getValue(u), getValue(z), step
end




#------------------- sub state estimation-------------------
function SEcb(msg::Odometry)
    # update mpc initial condition 
    global Getpos = true
    X[1] =    msg.pose.pose.position.x
    X[2] =    msg.pose.pose.position.y
    X[3] =    msg.pose.pose.orientation.w
    #X[4] =    msg.twist.twist.linear.x
    
end


#--------------  Find the nearest point on the reference of the car ----------------
function find_nearest(x,f,start)
    #print(x[1:2])
    #print(f[1:2,1])
    dis = Array(Float64,size(f,1))
    ref = Array(Float64,T)
    #print(size(dis))
    for i in 1:size(f,1)
        dis[i] = euclidean(x[1:2],f[i,1:2])
    end

    refstep=4
    ref_start = indmin(dis)
    if ref_start <= start
       ref_start = start+1 
     end
    print(ref_start)
        
    if (ref_start > size(f,1) - T*refstep) && (ref_start < size(f,1))
        #print(size(f,1)-ref_start)
	r=(size(f,1)-ref_start)%refstep
	if r != 0
                   ref = [ f[ref_start:refstep:size(f,1)-r,:] ; f[refstep-r:refstep:(T*refstep-(size(f,1)-ref_start)+r),:]   ]
               else
	    ref = [ f[ref_start:refstep:size(f,1),:] ; f[1:refstep:1+(T*refstep-(size(f,1)-ref_start)),:]   ]
                end
    elseif ref_start > size(f,1)
        ref_start = ref_start - size(f,1)
        ref = f[ref_start:refstep:ref_start+T*refstep,:]
    elseif ref_start == size(f,1)
	ref = f[1:refstep:T*refstep+1,:]
    else     
        ref = f[ref_start:refstep:ref_start+T*refstep,:]
        #print(ref)
    end
    
    
    return ref,ref_start
end

#--------------------Main function-----------------------------
function main()
    zT = [0;1.7;1/2*pi]  # Initial state - COO
    Xb =[0;2;pi]
    step=0
    # initiate node, set up publisher / subscriber topic
    init_node("mpc_parking")
    pub_car_cmd = Publisher("mpc/car_cmd", Twist2DStamped, queue_size=1)
    pub_first_refp = Publisher("goal", PointStamped, queue_size=1)
    sub  = Subscriber{Odometry}("euler_odom",  SEcb, queue_size=1)
    c1=1
    loop_rate = Rate(10)
    
    while ! is_shutdown()
        #print(X)
        if Getpos == true
            # find the nearest point on the path# get reference in horizon
            if step == T
            car_control_msg = Twist2DStamped()
            car_control_msg.v = 0
            car_control_msg.omega = 0
            #print(v)
            #publish commands
            publish(pub_car_cmd, car_control_msg)
                return
            end
            #Xb[1] = X[1] - l/2*cos(pi/2) + l/2*sin(X[3])
            #Xb[2] = X[2] - l/2*sin(pi/2) + l/2*cos(X[3])
            #Xb[3] = X[3]
            ## run mpc, publish command
            u_vec, z_vec, step = solveMPC(l,n,m,T-step,X,zT,zmax,umax,dt, step)

            println("solve!")
            #print(u_vec[1,1] ,u_vec[1,2])

            # get optimal solutions
            v_opt   = u_vec[1,2]
            d_f_opt = u_vec[1,1]

            #v = v_opt*sqrt(1+c1*c1*d_f_opt*d_f_opt)
            w = -v_opt/l*d_f_opt
            car_control_msg = Twist2DStamped()
            car_control_msg.v = v_opt 
            car_control_msg.omega = w
            #print(v)
            #publish commands
            publish(pub_car_cmd, car_control_msg)
        else
            println("unknown position")    
        end
        rossleep(loop_rate)
    end
    spin()
end

if ! isinteractive()   
    main()
end
