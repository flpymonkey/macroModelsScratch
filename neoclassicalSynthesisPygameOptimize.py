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
scenario_name = "1:Baseline"

# Create arrays to store equilibrium solutions from different parameterizations
Y_star = 0  # Income/output
C_star = 0  # Consumption
I_star = 0  # Investment
r_star = 0  # Real interest rate
N_star = 0  # Employment
U_star = 0  # Unemployment rate
P_star = 0  # Price level
w_star = 0  # Real wage
W_star = 0  # Nominal wage

# Construct different scenarios
# baseline
A = 2
i0 = 2
M0 = 5
G0 = 1
P0 = 1

# Set constant parameter values
c0 = 2  # Autonomous consumption
c1 = 0.6  # Sensitivity of consumption with respect to income (marginal propensity to consume)
i1 = 0.1  # Sensitivity of investment with respect to the interest rate
m1 = 0.2  # Sensitivity of money demand with respect to income
m2 = 0.4  # Sensitivity of money demand with respect to interest rate
Nf = 5  # Full employment/labor force
K = 4  # Exogenous capital stock
a = 0.3  # Capital elasticity of output
b = 0.4  # Household preference for leisure
T0 = 1  # Tax revenues
m0 = 6  # Liquidity preference

# Initialize endogenous variables at some arbitrary positive value
Y = C = I = r = P = w = N = W = 1
##################

##################
# Show graph of the economy
# https://macrosimulation.org/a_neoclassical_synthesis_model_is_lm_as_ad#directed-graph
##################

def iterate_economy(C, I, G0, c0, c1, Y, T0, i0, i1, r, m0, M0, P, m2, m1, N, Nf, A, a, K, P0, b):
        '''
        sim_no: Simulation number (for saving simulation states in different scenarios)
        C: Consumption
        I: Investment
        G0: Government expendeture
        c0: Autonomous consumption
        c1: Sensitivity of consumption with respect to income (marginal propensity to consume)
        Y: Output of the economy
        T0: Tax revenues
        i0: Autonomous investment (animal spirits)
        i1: Sensitivity of investment with respect to the interest rate
        r: Real intrest rate
        m0: Liquidity prefrence
        M0: Money supply
        P: Price level
        m2: Sensitivity of money demand with respect to interest rate
        m1: Sensitivity of money demand with respect to income
        N: Employment 
        Nf: Full employment/labor force
        A: Productivity shifter (technology)
        a: Capital elasticity of output
        K: Exogenous capital stock
        P0: Expected price level
        b: Household preference for leisure
        '''
                
        # Model equations
        # Goods market equilibrium
        Y = C + I + G0

        # Consumption demand
        C = c0 + c1 * (Y - T0)

        # Investment demand
        I = i0 - i1 * r

        # Money market, solved for interest rate
        r = (m0 - (M0 / P)) / m2 + m1 * Y / m2

        # Unemployment rate
        U = 1 - N / Nf

        # Real wage
        w = A * (1 - a) * (K ** a) * (N ** (-a))

        # Nominal wage
        W = (P0 * b * C) / (1 - (N / Nf))

        # Price level
        P = W / w

        # Employment
        N = (Y / (A * (K ** a))) ** (1 / (1 - a))

        return Y, C, I, r, U, w, W, P, N

# Enable this to automatically iterate
AUTO_ITERATIOM = True

# Maximum number of iterations to display in each graph
MAX_PLOT_LENGTH = 50



# Count number of iterations for this simulation
iteration_count = 0
is_iter = False
in_sim = True

# Used for plotting the simulation over time
Y_time = []
P_time = []
N_time = []
C_time = []
I_time = []

# Append initial value
Y_time.append(Y)
P_time.append(P)
N_time.append(N)
C_time.append(C)
I_time.append(I)

# graph images to render
employment_surf = None
price_surf = None
output_surf = None
consumption_surf = None
investment_surf = None

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space bar pressed!")
                is_iter = True
            if event.key == pygame.K_w:
                print("w pressed!")
                i0 += 0.1
            if event.key == pygame.K_s:
                print("s pressed!")
                i0 -= 0.1
            if event.key == pygame.K_e:
                print("e pressed!")
                A += 0.1
            if event.key == pygame.K_d:
                print("d pressed!")
                A -= 0.1
            if event.key == pygame.K_r:
                print("r pressed!")
                G0 += 0.1
            if event.key == pygame.K_f:
                print("f pressed!")
                G0 -= 0.1
            if event.key == pygame.K_t:
                print("t pressed!")
                M0 += 0.1
            if event.key == pygame.K_g:
                print("g pressed!")
                M0 -= 0.1
        
        # Player has triggered an iteration
        if is_iter or AUTO_ITERATIOM:
            # Run economy updates
            Y, C, I, r, U, w, W, P, N = iterate_economy(C, I, G0, c0, c1, Y, T0, i0, i1, r, m0, M0, P, m2, m1, N, Nf, A, a, K, P0, b)
            # Save results for different parameterizations in the arrays
            Y_star = Y
            w_star = w
            C_star = C
            I_star = I
            r_star = r
            N_star = N
            P_star = P

            C_time.append(C)
            P_time.append(P)
            N_time.append(N)
            I_time.append(I)
            Y_time.append(Y)
            iteration_count += 1

            ###########################
            plot_min = max(0, iteration_count - MAX_PLOT_LENGTH)
            plot_max = iteration_count

            # Rerender the graph images
            ## TODO need to fix these ugly plots!!!!!!!!
            # Plot output
            plt.plot(Y_time, color='black', linewidth=2, linestyle='-')
            plt.xlabel("Time")
            plt.ylabel("Y")
            plt_title = scenario_name + ": Output"
            plt.title(plt_title, fontsize=10)
            plt.xlim((plot_min, plot_max))
            fig = plt.figure(plt_title)
            fig.set_figwidth(5)
            fig.set_figheight(4)

            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()

            size = canvas.get_width_height()
            output_surf = pygame.image.fromstring(raw_data, size, "RGB")
            # Clear the plot
            plt.clf()

                # Plot consumption
            plt.plot(C_time, color='black', linewidth=2, linestyle='-')
            plt.xlabel("Time")
            plt.ylabel("Consumption")
            plt_title = scenario_name + ": Consumption"
            plt.title(plt_title, fontsize=10)
            plt.xlim((plot_min, plot_max))
            fig = plt.figure(plt_title)
            fig.set_figwidth(5)
            fig.set_figheight(4)

            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()

            size = canvas.get_width_height()
            consumption_surf = pygame.image.fromstring(raw_data, (size), "RGB")
            # Clear the plot
            plt.clf()

            # Plot investment
            plt.plot(I_time, color='black', linewidth=2, linestyle='-')
            plt.xlabel("Time")
            plt.ylabel("Investment")
            plt_title = scenario_name + ": Investment"
            plt.title(plt_title, fontsize=10)
            plt.xlim((plot_min, plot_max))
            fig = plt.figure(plt_title)
            fig.set_figwidth(5)
            fig.set_figheight(4)

            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()

            size = canvas.get_width_height()

            investment_surf = pygame.image.fromstring(raw_data, size, "RGB")
            investment_surf = pygame.transform.scale(investment_surf, (400, 360))
            # Clear the plot
            plt.clf()

            # Plot price level
            plt.plot(P_time, color='black', linewidth=2, linestyle='-')
            plt.xlabel("Time")
            plt.ylabel("Price")
            plt_title = scenario_name + ": Price"
            plt.title(plt_title, fontsize=10)
            plt.xlim((plot_min, plot_max))
            fig = plt.figure(plt_title)
            fig.set_figwidth(5)
            fig.set_figheight(4)

            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()

            size = canvas.get_width_height()

            price_surf = pygame.image.fromstring(raw_data, size, "RGB")
            price_surf = pygame.transform.scale(price_surf, (400, 360))
            # Clear the plot
            plt.clf()

            # Plot employment level
            plt.plot(N_time, color='black', linewidth=2, linestyle='-')
            plt.xlabel("Time")
            plt.ylabel("Employment")
            plt_title = scenario_name + ": Employment"
            plt.title(plt_title, fontsize=10)
            plt.xlim((plot_min, plot_max))
            fig = plt.figure(plt_title)
            fig.set_figwidth(5)
            fig.set_figheight(4)

            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()

            size = canvas.get_width_height()

            employment_surf = pygame.image.fromstring(raw_data, size, "RGB")
            employment_surf = pygame.transform.scale(employment_surf, (400, 360))
            # Clear the plot
            plt.clf()
            ##########################
            
            # Wait for next iteration from player
            is_iter = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        #########################
        # Update economic visuals
        #########################

        # Add simple text
        iterate_text_surface = my_font.render('Press the space bar to iterate the economy', True, (255, 255, 255))
        sim_text_surface = my_font.render(scenario_name, True, (255, 255, 255))
        Y_text_surface = my_font.render('Y: ' + str(Y_star), True, (255, 255, 255))
        i0_text_surface = my_font.render('Autonomous investment: ' + str(i0), True, (255, 255, 255))
        A_text_surface = my_font.render('Productivity shifter: ' + str(A), True, (255, 255, 255))
        G0_text_surface = my_font.render('Government expenditure: ' + str(G0), True, (255, 255, 255))
        M0_text_surface = my_font.render('Money supply: ' + str(M0), True, (255, 255, 255))
        iter_text_surface = my_font.render('Iteration number: ' + str(iteration_count), True, (255, 255, 255))

        # Render text on the page at the specified positions
        screen.blit(iterate_text_surface, (50, 10)) 
        screen.blit(sim_text_surface, (50, 100)) 
        screen.blit(Y_text_surface, (50, 150))
        screen.blit(i0_text_surface, (50, 200))
        screen.blit(A_text_surface, (50, 250))
        screen.blit(G0_text_surface, (50, 300)) 
        screen.blit(M0_text_surface, (50, 350)) 
        screen.blit(iter_text_surface, (50, 600)) 

        if (iteration_count > 0):
            # add the graph images to the screen
            screen.blit(output_surf, (1200,0))
            screen.blit(consumption_surf, (1200,400))
            screen.blit(investment_surf, (800,0))
            screen.blit(price_surf, (800,360))
            screen.blit(employment_surf, (400,350))
        ##########################

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 30
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(30) / 1000

pygame.quit()