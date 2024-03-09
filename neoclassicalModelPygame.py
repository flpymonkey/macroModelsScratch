import pygame
import numpy as np

##################
# pygame setup
##################
pygame.init()
screen = pygame.display.set_mode((1720, 980))
clock = pygame.time.Clock()
running = True
dt = 0

# Fonts
my_font = pygame.font.SysFont('Comic Sans MS', 30)
##################


##################
# Matplotlib setup
# Within pygame, see article here:
# 
##################
import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
##################


##################
# economy setup
##################
# Set the number of scenarios (including baseline)
S = 6
scenario_names = ["1: Baseline", "2: Increase in M0", "3: Increase in G0", 
                  "4: Increase in A", "5: Decrease in Yf", "6: Increase in b1"]

# Create arrays to store equilibrium solutions from different parameterizations
Y_star = np.empty(S)  # Income/output
w_star = np.empty(S)  # Real wage
C_star = np.empty(S)  # Consumption
I_star = np.empty(S)  # Investment
r_star = np.empty(S)  # Real interest rate
rn_star = np.empty(S)  # Nominal interest rate
N_star = np.empty(S)  # Employment
P_star = np.empty(S)  # Price level

# Create and parameterize exogenous variables/parameters that will be shifted
M0 = np.zeros(S)  # Money supply
G0 = np.zeros(S)  # Government expenditures
A = np.zeros(S)   # Productivity
Yf = np.zeros(S)  # Expected future income
leisure = np.zeros(S)  # Household preference for leisure (b1)

# Baseline parameterisation
M0[:] = 5
G0[:] = 1
A[:] = 2
Yf[:] = 1
leisure[:] = 0.4

# Set parameter values for different scenarios
M0[1] = 6   # Scenario 2: monetary expansion
G0[2] = 2   # Scenario 3: fiscal expansion
A[3] = 2.5  # Scenario 4: productivity boost
Yf[4] = 0.2  # Scenario 5: lower expected future income
leisure[5] = 0.8  # Scenario 6: increased preference for leisure

# Set constant parameter values
a = 0.3  # Capital elasticity of output
discount_rate = 0.9  # Discount rate
money_pref = 0.6  # Household preference for money
K = 5  # Exogenous capital stock
pe = 0.02  # Expected rate of inflation
Gf = 1  # Future government spending

# Initialize endogenous variables at arbitrary positive values
w = C = I = Y = r = N = P = 1 
##################

def iterate_economy(i, A, a, K, N, I, leisure, discount_rate, money_pref, G0, Yf, Gf, r, M0):
        '''
        i: Simulation index
        A: Productivity shifter
        a: Capital elasticity of output
        K: Exogenous capital stock
        N: Labour supply
        I: Investment
        leisure: Household preference for leisure
        discount_rate: ??????????????
        money_pref: Household preference for money ????????????
        G0: Government expenditures
        Yf: Expected future income
        Gf: Future government spending
        r: Real interest rate ?
        M0: Money supply
        '''
        # (1) Cobb-Douglas production function
        Y = A[i] * (K**a) * N**(1-a)

        # (2) Labour demand
        w = A[i] * (1-a) * (K**a) * N**(-a)

        # (3) Labour supply
        N = 1 - (leisure[i]) / w

        # (4) Consumption demand
        C = (1 / (1 + discount_rate + money_pref)) * (Y - G0[i] + (Yf[i] - Gf) / (1 + r) - leisure[i] * (discount_rate + money_pref) * np.log(leisure[i] / w))

        # (5) Investment demand, solved for r
        r = (I**(a-1)) * a * A[i] * N**(1-a)

        # (6) Goods market equilibrium condition, solved for I
        I = Y - C - G0[i]

        # (7) Nominal interest rate
        rn = r + pe

        # (8) Price level
        P = (M0[i] * rn) / ((1 + rn) * money_pref * C)

        return Y, w, N, C, r, I, rn, P

for sim_no in range(S):

    # User is closing pygame
    if not running:
        break

    # Count number of iterations for this simulation
    iteration_count = 0
    is_iter = False
    in_sim = True

    # Used for plotting the simulation over time
    Y_time = []
    P_time = []
    C_time = []
    I_time = []

    # Append initial value
    Y_time.append(Y)
    P_time.append(P)
    C_time.append(C)
    I_time.append(I)

    while in_sim and running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space bar pressed!")
                    is_iter = True
                if event.key == pygame.K_q:
                    print("q pressed!")
                    print("Simulation ended")
                    in_sim = False
                if event.key == pygame.K_w:
                    print("w pressed!")
                    leisure[sim_no] += 0.1
                if event.key == pygame.K_s:
                    print("s pressed!")
                    leisure[sim_no] -= 0.1
                if event.key == pygame.K_e:
                    print("e pressed!")
                    A[sim_no] += 0.1
                if event.key == pygame.K_d:
                    print("d pressed!")
                    A[sim_no] -= 0.1
                if event.key == pygame.K_r:
                    print("r pressed!")
                    G0[sim_no] += 0.1
                if event.key == pygame.K_f:
                    print("f pressed!")
                    G0[sim_no] -= 0.1
                if event.key == pygame.K_t:
                    print("t pressed!")
                    M0[sim_no] += 0.1
                if event.key == pygame.K_g:
                    print("g pressed!")
                    M0[sim_no] -= 0.1
            
            # Player has triggered an iteration
            if is_iter:
                # Run economy updates
                Y, w, N, C, r, I, rn, P = iterate_economy(sim_no, A, a, K, N, I, leisure, discount_rate, money_pref, G0, Yf, Gf, r, M0)
                # Save results for different parameterizations in the arrays
                Y_star[sim_no] = Y
                w_star[sim_no] = w
                C_star[sim_no] = C
                I_star[sim_no] = I
                r_star[sim_no] = r
                N_star[sim_no] = N
                P_star[sim_no] = P
                rn_star[sim_no] = rn

                C_time.append(C)
                P_time.append(P)
                I_time.append(I)
                Y_time.append(Y)
                iteration_count += 1
                # Wait for next iteration from player
                is_iter = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("purple")

            #########################
            # Update economic visuals
            #########################

            # Add simple text
            iterate_text_surface = my_font.render('Press the space bar to iterate the economy', True, (255, 255, 255))
            sim_text_surface = my_font.render(scenario_names[sim_no], True, (255, 255, 255))
            Y_text_surface = my_font.render('Y: ' + str(Y_star[sim_no]), True, (255, 255, 255))
            leisure_text_surface = my_font.render('leisure prefence: ' + str(leisure[sim_no]), True, (255, 255, 255))
            A_text_surface = my_font.render('Productivity shifter: ' + str(A[sim_no]), True, (255, 255, 255))
            G0_text_surface = my_font.render('Government expenditure: ' + str(G0[sim_no]), True, (255, 255, 255))
            M0_text_surface = my_font.render('Money supply: ' + str(M0[sim_no]), True, (255, 255, 255))
            iter_text_surface = my_font.render('Iteration number: ' + str(iteration_count), True, (255, 255, 255))

            # Render text on the page at the specified positions
            screen.blit(iterate_text_surface, (50, 10)) 
            screen.blit(sim_text_surface, (50, 100)) 
            screen.blit(Y_text_surface, (50, 150))
            screen.blit(leisure_text_surface, (50, 200))
            screen.blit(A_text_surface, (50, 250))
            screen.blit(G0_text_surface, (50, 300)) 
            screen.blit(M0_text_surface, (50, 350)) 
            screen.blit(iter_text_surface, (50, 600)) 

            if (iteration_count > 0):

                ## TODO need to fix these ugly plots!!!!!!!!
                # Plot output
                plt.plot(Y_time[0:iteration_count], color='black', linewidth=2, linestyle='-')
                plt.xlabel("Time")
                plt.ylabel("Y")
                plt_title = scenario_names[sim_no] + ": Output"
                plt.title(plt_title, fontsize=10)
                fig = plt.figure(plt_title)
                fig.set_figwidth(5)
                fig.set_figheight(4)

                canvas = agg.FigureCanvasAgg(fig)
                canvas.draw()
                renderer = canvas.get_renderer()
                raw_data = renderer.tostring_rgb()

                size = canvas.get_width_height()

                surf = pygame.image.fromstring(raw_data, size, "RGB")
                screen.blit(surf, (1200,0))

                # Plot consumption
                plt.plot(C_time[0:iteration_count], color='black', linewidth=2, linestyle='-')
                plt.xlabel("Time")
                plt.ylabel("Consumption")
                plt_title = scenario_names[sim_no] + ": Consumption"
                plt.title(plt_title, fontsize=10)
                fig = plt.figure(plt_title)
                fig.set_figwidth(5)
                fig.set_figheight(4)

                canvas = agg.FigureCanvasAgg(fig)
                canvas.draw()
                renderer = canvas.get_renderer()
                raw_data = renderer.tostring_rgb()

                size = canvas.get_width_height()

                surf = pygame.image.fromstring(raw_data, (size), "RGB")
                screen.blit(surf, (1200,400))

                # Plot investment
                plt.plot(I_time[0:iteration_count], color='black', linewidth=2, linestyle='-')
                plt.xlabel("Time")
                plt.ylabel("Investment")
                plt_title = scenario_names[sim_no] + ": Investment"
                plt.title(plt_title, fontsize=10)
                fig = plt.figure(plt_title)
                fig.set_figwidth(5)
                fig.set_figheight(4)

                canvas = agg.FigureCanvasAgg(fig)
                canvas.draw()
                renderer = canvas.get_renderer()
                raw_data = renderer.tostring_rgb()

                size = canvas.get_width_height()

                surf = pygame.image.fromstring(raw_data, size, "RGB")
                surf = pygame.transform.scale(surf, (400, 360))
                screen.blit(surf, (800,100))

                # Plot price level
                plt.plot(P_time[0:iteration_count], color='black', linewidth=2, linestyle='-')
                plt.xlabel("Time")
                plt.ylabel("Price")
                plt_title = scenario_names[sim_no] + ": Price"
                plt.title(plt_title, fontsize=10)
                fig = plt.figure(plt_title)
                fig.set_figwidth(5)
                fig.set_figheight(4)

                canvas = agg.FigureCanvasAgg(fig)
                canvas.draw()
                renderer = canvas.get_renderer()
                raw_data = renderer.tostring_rgb()

                size = canvas.get_width_height()

                surf = pygame.image.fromstring(raw_data, size, "RGB")
                surf = pygame.transform.scale(surf, (400, 360))
                screen.blit(surf, (800,460))
            ##########################

            # flip() the display to put your work on screen
            pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()