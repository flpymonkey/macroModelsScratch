import pygame
import numpy as np

##################
# pygame setup
##################
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Fonts
my_font = pygame.font.SysFont('Comic Sans MS', 30)
##################


##################
# economy setup
##################
# Set the number of scenarios (including baseline)
S = 6

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

def iterate_economy(i, A, a, K, N, I, leisure, discount_rate, money_pref, G0, Yf, Gf, r):
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
    interation_count = 0
    is_iter = False
    in_sim = True

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
                if event.key == pygame.K_e:
                    print("e pressed!")
                    in_sim = False
            
            # Player has triggered an iteration
            if is_iter:
                # Run economy updates
                Y, w, N, C, r, I, rn, P = iterate_economy(sim_no, A, a, K, N, I, leisure, discount_rate, money_pref, G0, Yf, Gf, r)
                # Save results for different parameterizations in the arrays
                Y_star[sim_no] = Y
                w_star[sim_no] = w
                C_star[sim_no] = C
                I_star[sim_no] = I
                r_star[sim_no] = r
                N_star[sim_no] = N
                P_star[sim_no] = P
                rn_star[sim_no] = rn
                
                interation_count += 1
                # Wait for next iteration from player
                is_iter = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("purple")

            # Update economic visuals
            #Add simple text
            iterate_text_surface = my_font.render('Press the space bar to iterate the economy', True, (255, 255, 255))
            Y_text_surface = my_font.render('Y: ' + str(Y_star[sim_no]), True, (255, 255, 255))
            iter_text_surface = my_font.render('Iteration number: ' + str(interation_count), True, (255, 255, 255))

            # Render text on the page at the specified positions
            screen.blit(iterate_text_surface, (50, 10)) 
            screen.blit(Y_text_surface, (50, 100)) 
            screen.blit(iter_text_surface, (50, 600)) 

            # flip() the display to put your work on screen
            pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()