import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# plate size, mm
w = h = 304.8
# intervals in x-, y- directions, mm
dx = dy = 1
# Thermal diffusivity of Cu, mm2.s-1
D = 123

Tcool, Thot = 0, 15

nx, ny = int(w/dx), int(h/dy)

dx2, dy2 = dx*dx, dy*dy
dt = dx2 * dy2 / (2 * D * (dx2 + dy2))

# Initial conditions - ring of inner radius r, width dr centred at (cx,cy) (mm)
r, cx, cy = 8.8, 130, 130
r2 = r**2

def export_excel(u,filename):
    # Load spreadsheet
    df2 = pd.DataFrame(u.copy()[130])
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df2.to_excel(writer,'Sheet1',index=False)
    writer.save()

def do_timestep(u0, u, m):
    current_time = m*dt
    if (current_time < 2): # Heating time

 #       for i in range(nx): # Fills in inner circle with Tmax (use phenomenological here)
 #           for j in range(ny):
 #               p2 = (i*dx-cx)**2 + (j*dy-cy)**2
 #               if p2 < r2: 
        # Using phenomenological equation here to set center pixels (square
        u0[121:139,121:139] = 9.6 + -10.66*math.exp(-1.49*current_time)
        
    # Propagate with forward-difference in time, central-difference in space
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * (
          (u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2
          + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )

    u0 = u.copy()
    return u0, u

def main():

    # This is the grid 
    u0 = Tcool * np.ones((nx, ny))
    u = np.empty((nx, ny))

    # Number of timesteps
    nsteps = 1100

    # Output 4 figures at these timesteps
    mfig = [100]
    fignum = 1
    fig = plt.figure()
    ax = fig.add_subplot(220 + fignum)

    for m in range(nsteps):
        print(m*dt)
        u0, u = do_timestep(u0, u, m)


        # export_excel(u,"thermalData2.xlsx") # export data to excel
        if (m%20 == 0):
            im = ax.imshow(u.copy(), cmap=plt.get_cmap('hot'), vmin=Tcool,vmax=Thot)
            plt.pause(0.001)
            print(m*dt)
    
    ax.axis([90,170,75,175])
    ax.set_title('{:.2f} s'.format(m*dt))
    fig.subplots_adjust(right=0.85)
    cbar_ax = fig.add_axes([0.9, 0.15, 0.03, 0.7])
    cbar_ax.set_xlabel('K', labelpad=20)
    fig.colorbar(im, cax=cbar_ax)

    plt.show()

if __name__ == "__main__":
    main()