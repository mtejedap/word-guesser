#
# Matias Tejeda Astaburuaga
# Word Guesser
#

# Import graphics and random libraries

from graphics import *
import random

# Define main() function. It accepts no arguments and returns no values

def main():

    # Create the control panel graphics window

    control_panel_objects = control_panel()

    # Initialize variables

    score = 0
    game_round = 1

    # Check for a click on the new or quit controls

    while True:

        try:
            
            if control_panel_objects[0] == None:
                
                break

            click = control_panel_objects[0].checkMouse()
    
            if click != None:
            
                click_x = click.getX()
                click_y = click.getY()

                # If the new control is clicked:

                if click_x > 25 and click_x < 105 and click_y > 50 and click_y < 90:

                    # Create an infinite loop that only stops under certain results in the game

                    while True:

                        # Call the game() function which starts the game

                        status,score,game_round = game(control_panel_objects,score,game_round)

                        # If the user clicks quit inside the game, close the control panel window (game panel window was closed inside game()) and end the program

                        if status == "quit":
                    
                            control_panel_objects[0].close()
                            return

                        # If the user clicks new inside the game, reset the score and round number and continue the loop to start a new game

                        elif status == "new":

                            score = 0
                            game_round = 1
                            continue

                        # If the user loses, reset the score and round number and stop the loop and check for a click on the new or quit controls again

                        elif status == "defeat":

                            score = 0
                            game_round = 1
                            break

                        # If the user wins, increment the round number and continue the loop to start a new round

                        elif status == "victory":

                            game_round += 1
                            continue

                # If the quit control is clicked:

                elif (click_x > 295 and click_x < 375 and click_y > 50 and click_y < 90):

                    # Close the control panel window and end the program 

                    control_panel_objects[0].close()
                    return

                # If the high score control is clicked:
            
                elif (click_x > 140 and click_x < 260 and click_y > 350 and click_y < 390):

                    # Call highscore() function

                    highscore()

        except GraphicsError:

            break

# Define game() function. It accepts three arguments and return three values

def game(control_panel_objects,score,game_round):

    # Create the game panel graphics window

    game_panel_objects = game_panel()

    # Initialize variables
    
    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    circle_check = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    secret_word_completion = 0
    clicked_hint = False

    # If this is round 1, set the player's score to 10

    if game_round == 1:
        score = 10

    # If this is not round 1, add 10 points to the player's score
        
    elif game_round > 1:
        score += 10

    # Create a score message at the top of the game panel window

    score_message = Text(Point(400,30),"SCORE: "+str(score))
    score_message.setSize(20)
    score_message.draw(game_panel_objects[0])

    # Check for clicks on the new or quit controls or any of the black circles

    while True == True:

        click = control_panel_objects[0].checkMouse()
        click2 = game_panel_objects[0].checkMouse()
    
        if click != None:
            
            click_x = click.getX()
            click_y = click.getY()

            # If new control is clicked:

            if click_x > 25 and click_x < 105 and click_y > 50 and click_y < 90:

                # Close the game panel window

                game_panel_objects[0].close()

                # Return to main() with results
                
                status = "new"
                return status,score,game_round

            # If quit control is clicked:

            elif (click_x > 295 and click_x < 375 and click_y > 50 and click_y < 90):

                # Close the game panel window

                game_panel_objects[0].close()

                # Return to main() with results
                
                status = "quit"
                return status,score,game_round

            # If the hint control is clicked:

            elif (click_x > 160 and click_x < 240 and click_y > 50 and click_y < 90) and clicked_hint == False:

                # Disable hint control

                clicked_hint = True

                # Initialize variables
                
                count = 0

                # Create a while loop that shows three random incorrect circles and disables them

                while count != 3:

                    incorrect = random.choice(game_panel_objects[1])

                    test_letter = alphabet[game_panel_objects[1].index(incorrect)]

                    game_panel_objects[5] = game_panel_objects[5].lower()

                    if test_letter not in game_panel_objects[5] and circle_check[game_panel_objects[1].index(incorrect)] == False:

                        incorrect.setFill("gold")
                        game_panel_objects[2][game_panel_objects[1].index(incorrect)].setTextColor("black")
                        circle_check[game_panel_objects[1].index(incorrect)] = True
                        count += 1

                # If there's one polygon remaining, reduce the score by one and drop one polygon

                if len(game_panel_objects[4]) == 1:

                    score -= 1
                    score_message.setText("SCORE: "+str(score))
                        
                    drop(game_panel_objects[4][0])
                        
                    game_panel_objects[4][0].undraw()
                    del game_panel_objects[4][0]

                # If there's more than one polygon remaining, reduce the score by two and drop two polygons

                elif len(game_panel_objects[4]) > 1:

                    for i in range(2):

                        score -= 1
                        score_message.setText("SCORE: "+str(score))

                        drop(game_panel_objects[4][0])

                        game_panel_objects[4][0].undraw()
                        del game_panel_objects[4][0]

            # If the high score control is clicked:

            elif (click_x > 140 and click_x < 260 and click_y > 350 and click_y < 390):

                # Call highscore() function
                    
                highscore()
                    
        elif click2 != None:

            click2_x = click2.getX()
            click2_y = click2.getY()

            # Use a for loop that iterates through every black circle in order to check if a click happened inside

            for i in enumerate(game_panel_objects[1]):

                radius = i[1].getRadius()
                circle_center = i[1].getCenter()
                circle_x = circle_center.getX()
                circle_y = circle_center.getY()
                distance = ((click2_x - circle_x)**2 + (click2_y - circle_y)**2)**(1/2)

                # If a click is within one of the black circles, and the black circle isn't disabled:

                if distance < radius and circle_check[i[0]] == False:

                    # Change the clicked circle fill color to gold and the text character color to black

                    i[1].setFill("gold")
                    game_panel_objects[2][i[0]].setTextColor("black")

                    # Determine the character guessed
                    
                    guessed_letter = alphabet[i[0]]

                    # Change the index of the circle in the circle_check list to True, therefore disabling it
                    
                    circle_check[i[0]] = True

                    # Make the secret word lowercase for easier processing
                    
                    game_panel_objects[5] = game_panel_objects[5].lower()

                    # Initialize a variable that checks whether the guess was right or wrong
                    
                    guessed_right = False

                    # Create a for loop that iterates over the letters in the secret word

                    for i in enumerate(game_panel_objects[5]):

                        # If the guessed character is equal to one of the letters in the secret word:

                        if guessed_letter == i[1]:

                            # Get the center coordinates of the rectangle from the same index as the letter in the secret word

                            secret_letter_center = game_panel_objects[6][i[0]].getCenter()

                            # Create the letter in the secret word as a text object inside the respective rectangle
                            
                            secret_letter = Text(secret_letter_center,guessed_letter.upper())
                            secret_letter.setSize(20)
                            secret_letter.setStyle("bold")
                            secret_letter.draw(game_panel_objects[0])

                            # Increment the secret word completion by 1
                            
                            secret_word_completion += 1

                            # Update the variable with a right guess
                            
                            guessed_right = True

                    # If the user didn't guess any of the secret word letters right:

                    if guessed_right == False:

                        # Reduce the score by 1 and update the score message

                        score -= 1
                        score_message.setText("SCORE: "+str(score))

                        # Call the drop() function with the first index in the black polygon list
                        
                        drop(game_panel_objects[4][0])

                        # Undraw and delete the first index in the black polygon list after drop() is finished
                        
                        game_panel_objects[4][0].undraw()
                        del game_panel_objects[4][0]

        # If the black polygon list is empty:

        if game_panel_objects[4] == []:

            # Create bold, red text objects indicating the game is over

            defeat_message = Text(Point(400,400),"YOU LOSE - HAMMER DOWN!")
            defeat_message.setTextColor("red")
            defeat_message.setSize(20)
            defeat_message.setStyle("bold")

            # Create graphics objects that allow the user to input a name
            
            defeat_message.draw(game_panel_objects[0])
            defeat_rectangle = Rectangle(Point(250,430),Point(550,517))
            defeat_rectangle.setFill("black")
            defeat_rectangle.draw(game_panel_objects[0])
            defeat_entry = Entry(Point(400,450),25)
            defeat_entry.setFill("black")
            defeat_entry.setTextColor("gold")
            defeat_entry.setSize(15)
            defeat_entry.setText("Please enter your name")
            defeat_entry.draw(game_panel_objects[0])
            saver = Rectangle(Point(365,470),Point(435,510))
            saver.setFill("gold")
            saver.draw(game_panel_objects[0])
            savet = Text(Point(400,490),"SAVE")
            savet.setSize(15)
            savet.setStyle("bold")
            savet.draw(game_panel_objects[0])

            # Create an infinite loop that is stopped when a click is registered in the save button

            while True:

                click = game_panel_objects[0].checkMouse()
    
                if click != None:
            
                    click_x = click.getX()
                    click_y = click.getY()

                    if click_x > 365 and click_x < 435 and click_y > 470 and click_y < 510:

                        break

            # Get the name from the entry object

            name = defeat_entry.getText()

            # Open and append name, game round, and score to the scores.txt file

            infile = open("scores.txt","a")
            infile.write("\n"+name+","+str(game_round)+","+str(score))
            infile.close()

            # Close the game panel window

            game_panel_objects[0].close()

            # Return to main() with results

            status = "defeat"
            return status,score,game_round

        # If the secret word completion equals the length of the secret word:

        elif secret_word_completion == len(game_panel_objects[5]):

            # Create text objects indicating a winning round

            victory_message = Text(Point(400,400),"YOU WIN - BOILER UP!")
            victory_message.setTextColor("grey")
            victory_message.setSize(20)
            victory_message.setStyle("bold")
            victory_message.draw(game_panel_objects[0])
            victory_message2 = Text(Point(400,450),"Click to continue")
            victory_message2.setTextColor("grey")
            victory_message2.setStyle("italic")
            victory_message2.draw(game_panel_objects[0])

            # Wait for a mouse click inside the game panel window

            game_panel_objects[0].getMouse()

            # Close the game panel window

            game_panel_objects[0].close()

            # Return to main() with results

            status = "victory"
            return status,score,game_round
                        
# Define control_panel() function. It accepts no arguments and returns a list of graphics objects

def control_panel():

    # Create a graphics window with a light-grey background titled "Welcome to:"

    window1 = GraphWin("Welcome to:",400,415)
    window1.setBackground("light grey")

    # Create the graphics objects as shown in the example

    title = Rectangle(Point(0,0),Point(400,25))
    title.setFill("black")
    title.draw(window1)

    title_message = Text(Point(200,13.5),"WORD GUESSER")
    title_message.setTextColor("gold")
    title_message.setStyle("bold")
    title_message.setSize(15)
    title_message.draw(window1)

    new = Rectangle(Point(25,50),Point(105,90))
    new.setFill("gold")
    new.draw(window1)

    new_message = Text(Point(65,70),"NEW")
    new_message.setStyle("bold")
    new_message.draw(window1)

    quit1 = Rectangle(Point(295,50),Point(375,90))
    quit1.setFill("black")
    quit1.draw(window1)

    quit1_message = Text(Point(335,70),"QUIT")
    quit1_message.setTextColor("gold")
    quit1_message.setStyle("bold")
    quit1_message.draw(window1)

    body = Rectangle(Point(25,115),Point(375,250))
    body.setFill("white")
    body.draw(window1)

    body_message1 = Text(Point(200,162.5),"This is a game where your score is")
    body_message1.draw(window1)
    body_message2 = Text(Point(200,182.5),"based on the number of 4-6 letter")
    body_message2.draw(window1)
    body_message3 = Text(Point(200,202.5),"words you can guess within 10 tries.")
    body_message3.draw(window1)

    prompt_message = Text(Point(200,300),"Click NEW to start a game...")
    prompt_message.setSize(15)
    prompt_message.draw(window1)

    hint = Rectangle(Point(160,50),Point(240,90))
    hint.setFill("white")
    hint.draw(window1)

    hint_message = Text(Point(200,70),"HINT")
    hint_message.setStyle("bold")
    hint_message.draw(window1)

    highscorer = Rectangle(Point(140,350),Point(260,390))
    highscorer.setFill("dodgerblue")
    highscorer.draw(window1)

    highscoret = Text(Point(200,370),"HIGH SCORE")
    highscoret.setTextColor("light blue")
    highscoret.setStyle("bold")
    highscoret.draw(window1)

    # Create a list of the graphics objects for easy referencing

    control_panel_objects = [window1, title, title_message, new, new_message, quit1, quit1_message, body, body_message1, body_message2, body_message3, prompt_message, hint, hint_message]

    # Return the list

    return control_panel_objects

# Define game_panel() function. It accepts no arguments and returns a list of graphics objects

def game_panel():

    # Create a graphics window titled "Save the Block P" with a gold background

    window = GraphWin("Save the Block P",800,800)
    window.setBackground("gold")

    # Draw two rows of 13 black-filled Circles near the bottom of the window with single white letters within

    a = Circle(Point(49.2307692308,692.307692308),29.2307692308)
    a.setFill("black")
    a.draw(window)
    b = Circle(Point(107.6923077,692.307692308),29.2307692308)
    b.setFill("black")
    b.draw(window)
    c = Circle(Point(166.1538462,692.307692308),29.2307692308)
    c.setFill("black")
    c.draw(window)
    d = Circle(Point(224.6153846,692.307692308),29.2307692308)
    d.setFill("black")
    d.draw(window)
    e = Circle(Point(283.0769231,692.307692308),29.2307692308)
    e.setFill("black")
    e.draw(window)
    f = Circle(Point(341.5384615,692.307692308),29.2307692308)
    f.setFill("black")
    f.draw(window)
    g = Circle(Point(400,692.307692308),29.2307692308)
    g.setFill("black")
    g.draw(window)
    h = Circle(Point(458.4615385,692.307692308),29.2307692308)
    h.setFill("black")
    h.draw(window)
    i = Circle(Point(516.9230769,692.307692308),29.2307692308)
    i.setFill("black")
    i.draw(window)
    j = Circle(Point(575.3846154,692.307692308),29.2307692308)
    j.setFill("black")
    j.draw(window)
    k = Circle(Point(633.8461538,692.307692308),29.2307692308)
    k.setFill("black")
    k.draw(window)
    l = Circle(Point(692.3076923,692.307692308),29.2307692308)
    l.setFill("black")
    l.draw(window)
    m = Circle(Point(750.7692308,692.307692308),29.2307692308)
    m.setFill("black")
    m.draw(window)
    n = Circle(Point(49.2307692308,750.7692308),29.2307692308)
    n.setFill("black")
    n.draw(window)
    o = Circle(Point(107.6923077,750.7692308),29.2307692308)
    o.setFill("black")
    o.draw(window)
    p = Circle(Point(166.1538462,750.7692308),29.2307692308)
    p.setFill("black")
    p.draw(window)
    q = Circle(Point(224.6153846,750.7692308),29.2307692308)
    q.setFill("black")
    q.draw(window)
    r = Circle(Point(283.0769231,750.7692308),29.2307692308)
    r.setFill("black")
    r.draw(window)
    s = Circle(Point(341.5384615,750.7692308),29.2307692308)
    s.setFill("black")
    s.draw(window)
    t = Circle(Point(400,750.7692308),29.2307692308)
    t.setFill("black")
    t.draw(window)
    u = Circle(Point(458.4615385,750.7692308),29.2307692308)
    u.setFill("black")
    u.draw(window)
    v = Circle(Point(516.9230769,750.7692308),29.2307692308)
    v.setFill("black")
    v.draw(window)
    w = Circle(Point(575.3846154,750.7692308),29.2307692308)
    w.setFill("black")
    w.draw(window)
    x = Circle(Point(633.8461538,750.7692308),29.2307692308)
    x.setFill("black")
    x.draw(window)
    y = Circle(Point(692.3076923,750.7692308),29.2307692308)
    y.setFill("black")
    y.draw(window)
    z = Circle(Point(750.7692308,750.7692308),29.2307692308)
    z.setFill("black")
    z.draw(window)

    a_message = Text(Point(49.2307692308,692.307692308),"A")
    a_message.setTextColor("white")
    a_message.setSize(20)
    a_message.draw(window)
    b_message = Text(Point(107.6923077,692.307692308),"B")
    b_message.setTextColor("white")
    b_message.setSize(20)
    b_message.draw(window)
    c_message = Text(Point(166.1538462,692.307692308),"C")
    c_message.setTextColor("white")
    c_message.setSize(20)
    c_message.draw(window)
    d_message = Text(Point(224.6153846,692.307692308),"D")
    d_message.setTextColor("white")
    d_message.setSize(20)
    d_message.draw(window)
    e_message = Text(Point(283.0769231,692.307692308),"E")
    e_message.setTextColor("white")
    e_message.setSize(20)
    e_message.draw(window)
    f_message = Text(Point(341.5384615,692.307692308),"F")
    f_message.setTextColor("white")
    f_message.setSize(20)
    f_message.draw(window)
    g_message = Text(Point(400,692.307692308),"G")
    g_message.setTextColor("white")
    g_message.setSize(20)
    g_message.draw(window)
    h_message = Text(Point(458.4615385,692.307692308),"H")
    h_message.setTextColor("white")
    h_message.setSize(20)
    h_message.draw(window)
    i_message = Text(Point(516.9230769,692.307692308),"I")
    i_message.setTextColor("white")
    i_message.setSize(20)
    i_message.draw(window)
    j_message = Text(Point(575.3846154,692.307692308),"J")
    j_message.setTextColor("white")
    j_message.setSize(20)
    j_message.draw(window)
    k_message = Text(Point(633.8461538,692.307692308),"K")
    k_message.setTextColor("white")
    k_message.setSize(20)
    k_message.draw(window)
    l_message = Text(Point(692.3076923,692.307692308),"L")
    l_message.setTextColor("white")
    l_message.setSize(20)
    l_message.draw(window)
    m_message = Text(Point(750.7692308,692.307692308),"M")
    m_message.setTextColor("white")
    m_message.setSize(20)
    m_message.draw(window)
    n_message = Text(Point(49.2307692308,750.7692308),"N")
    n_message.setTextColor("white")
    n_message.setSize(20)
    n_message.draw(window)
    o_message = Text(Point(107.6923077,750.7692308),"O")
    o_message.setTextColor("white")
    o_message.setSize(20)
    o_message.draw(window)
    p_message = Text(Point(166.1538462,750.7692308),"P")
    p_message.setTextColor("white")
    p_message.setSize(20)
    p_message.draw(window)
    q_message = Text(Point(224.6153846,750.7692308),"Q")
    q_message.setTextColor("white")
    q_message.setSize(20)
    q_message.draw(window)
    r_message = Text(Point(283.0769231,750.7692308),"R")
    r_message.setTextColor("white")
    r_message.setSize(20)
    r_message.draw(window)
    s_message = Text(Point(341.5384615,750.7692308),"S")
    s_message.setTextColor("white")
    s_message.setSize(20)
    s_message.draw(window)
    t_message = Text(Point(400,750.7692308),"T")
    t_message.setTextColor("white")
    t_message.setSize(20)
    t_message.draw(window)
    u_message = Text(Point(458.4615385,750.7692308),"U")
    u_message.setTextColor("white")
    u_message.setSize(20)
    u_message.draw(window)
    v_message = Text(Point(516.9230769,750.7692308),"V")
    v_message.setTextColor("white")
    v_message.setSize(20)
    v_message.draw(window)
    w_message = Text(Point(575.3846154,750.7692308),"W")
    w_message.setTextColor("white")
    w_message.setSize(20)
    w_message.draw(window)
    x_message = Text(Point(633.8461538,750.7692308),"X")
    x_message.setTextColor("white")
    x_message.setSize(20)
    x_message.draw(window)
    y_message = Text(Point(692.3076923,750.7692308),"Y")
    y_message.setTextColor("white")
    y_message.setSize(20)
    y_message.draw(window)
    z_message = Text(Point(750.7692308,750.7692308),"Z")
    z_message.setTextColor("white")
    z_message.setSize(20)
    z_message.draw(window)

    # Create lists of the graphics objects for easy referencing

    circles = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]
    letters = [a_message,b_message,c_message,d_message,e_message,f_message,g_message,h_message,i_message,j_message,k_message,l_message,m_message,n_message,o_message,p_message,q_message,r_message,s_message,t_message,u_message,v_message,w_message,x_message,y_message,z_message]

    # Draw a series of 10 white and black Polygons to create the BLOCK P shape

    p1_white = Polygon(Point(198.7179487,579.4017094),Point(341.7948718,579.4017094),Point(338.4615385,633.0769231),Point(195.3846154,633.0769231))
    p1_white.setFill("white")
    p1_white.draw(window)
    p2_white = Polygon(Point(215.3846154,472.051282),Point(338.4615385,472.051282),Point(331.7948718,579.4017094),Point(208.7179487,579.4017094))
    p2_white.setFill("white")
    p2_white.draw(window)
    p3_white = Polygon(Point(222.0512821,364.7008546),Point(345.1282052,364.7008546),Point(338.4615385,472.051282),Point(215.3846154,472.051282))
    p3_white.setFill("white")
    p3_white.draw(window)
    p4_white = Polygon(Point(228.7179488,257.3504272),Point(351.7948719,257.3504272),Point(345.1282052,364.7008546),Point(222.0512821,364.7008546))
    p4_white.setFill("white")
    p4_white.draw(window)
    p5_white = Polygon(Point(235.3846155,150),Point(358.4615386,150),Point(351.7948719,257.3504272),Point(228.7179488,257.3504272))
    p5_white.setFill("white")
    p5_white.draw(window)
    p6_white = Polygon(Point(358.4615386,150),Point(481.5384617,150),Point(474.871795,257.3504272),Point(351.7948719,257.3504272))
    p6_white.setFill("white")
    p6_white.draw(window)
    p7_white = Polygon(Point(481.5384617,150),Point(604.6153848,150),Point(597.9487181,257.3504272),Point(474.871795,257.3504272))
    p7_white.setFill("white")
    p7_white.draw(window)
    p8_white = Polygon(Point(474.871795,257.3504272),Point(597.9487181,257.3504272),Point(591.2820514,364.7008546),Point(468.2051283,364.7008546))
    p8_white.setFill("white")
    p8_white.draw(window)
    p9_white = Polygon(Point(468.2051283,364.7008546),Point(591.2820514,364.7008546),Point(584.6153847,472.051282),Point(461.5384616,472.051282))
    p9_white.setFill("white")
    p9_white.draw(window)
    p10_white = Polygon(Point(345.1282052,364.7008546),Point(468.2051283,364.7008546),Point(461.5384616,472.051282),Point(338.4615385,472.051282))
    p10_white.setFill("white")
    p10_white.draw(window)

    p1_black = Polygon(Point(198.7179487,579.4017094),Point(341.7948718,579.4017094),Point(338.4615385,633.0769231),Point(195.3846154,633.0769231))
    p1_black.setFill("black")
    p1_black.draw(window)
    p2_black = Polygon(Point(215.3846154,472.051282),Point(338.4615385,472.051282),Point(331.7948718,579.4017094),Point(208.7179487,579.4017094))
    p2_black.setFill("black")
    p2_black.draw(window)
    p3_black = Polygon(Point(222.0512821,364.7008546),Point(345.1282052,364.7008546),Point(338.4615385,472.051282),Point(215.3846154,472.051282))
    p3_black.setFill("black")
    p3_black.draw(window)
    p4_black = Polygon(Point(228.7179488,257.3504272),Point(351.7948719,257.3504272),Point(345.1282052,364.7008546),Point(222.0512821,364.7008546))
    p4_black.setFill("black")
    p4_black.draw(window)
    p5_black = Polygon(Point(235.3846155,150),Point(358.4615386,150),Point(351.7948719,257.3504272),Point(228.7179488,257.3504272))
    p5_black.setFill("black")
    p5_black.draw(window)
    p6_black = Polygon(Point(358.4615386,150),Point(481.5384617,150),Point(474.871795,257.3504272),Point(351.7948719,257.3504272))
    p6_black.setFill("black")
    p6_black.draw(window)
    p7_black = Polygon(Point(481.5384617,150),Point(604.6153848,150),Point(597.9487181,257.3504272),Point(474.871795,257.3504272))
    p7_black.setFill("black")
    p7_black.draw(window)
    p8_black = Polygon(Point(474.871795,257.3504272),Point(597.9487181,257.3504272),Point(591.2820514,364.7008546),Point(468.2051283,364.7008546))
    p8_black.setFill("black")
    p8_black.draw(window)
    p9_black = Polygon(Point(468.2051283,364.7008546),Point(591.2820514,364.7008546),Point(584.6153847,472.051282),Point(461.5384616,472.051282))
    p9_black.setFill("black")
    p9_black.draw(window)
    p10_black = Polygon(Point(345.1282052,364.7008546),Point(468.2051283,364.7008546),Point(461.5384616,472.051282),Point(338.4615385,472.051282))
    p10_black.setFill("black")
    p10_black.draw(window)

    # Create lists of the graphics objects for easy referencing

    p_white = [p1_white,p2_white,p3_white,p4_white,p5_white,p6_white,p7_white,p8_white,p9_white,p10_white]
    p_black = [p1_black,p2_black,p3_black,p4_black,p5_black,p6_black,p7_black,p8_black,p9_black,p10_black]

    # Select a secret word from the words.txt datafile

    infile = open("words.txt","r")
    words = infile.readlines()
    infile.close()

    secret_word = random.choice(words)
    secret_word = secret_word.replace("\n","")
    secret_word_length = len(secret_word)

    # Draw a series of gold-filled Rectangles representing the characters in the secret word, and create a list of them for easy referencing

    if secret_word_length == 4:
        index1 = Rectangle(Point(240,60),Point(320,140))
        index1.draw(window)
        index2 = Rectangle(Point(320,60),Point(400,140))
        index2.draw(window)
        index3 = Rectangle(Point(400,60),Point(480,140))
        index3.draw(window)
        index4 = Rectangle(Point(480,60),Point(560,140))
        index4.draw(window)
        secret_word_rectangles = [index1,index2,index3,index4]
    if secret_word_length == 5:
        index1 = Rectangle(Point(200,60),Point(280,140))
        index1.draw(window)
        index2 = Rectangle(Point(280,60),Point(360,140))
        index2.draw(window)
        index3 = Rectangle(Point(360,60),Point(440,140))
        index3.draw(window)
        index4 = Rectangle(Point(440,60),Point(520,140))
        index4.draw(window)
        index5 = Rectangle(Point(520,60),Point(600,140))
        index5.draw(window)
        secret_word_rectangles = [index1,index2,index3,index4,index5]
    if secret_word_length == 6:
        index1 = Rectangle(Point(160,60),Point(240,140))
        index1.draw(window)
        index2 = Rectangle(Point(240,60),Point(320,140))
        index2.draw(window)
        index3 = Rectangle(Point(320,60),Point(400,140))
        index3.draw(window)
        index4 = Rectangle(Point(400,60),Point(480,140))
        index4.draw(window)
        index5 = Rectangle(Point(480,60),Point(560,140))
        index5.draw(window)
        index6 = Rectangle(Point(560,60),Point(640,140))
        index6.draw(window)
        secret_word_rectangles = [index1,index2,index3,index4,index5,index6]

    # Make a list of the lists of graphics objects and the secret word

    game_panel_objects = [window,circles,letters,p_white,p_black,secret_word,secret_word_rectangles]

    # Return the list

    return game_panel_objects

# Define drop() function. It accepts one argument and returns no values

def drop(p):

    # Change the fill color of the polygon to red

    p.setFill("red")

    # Animate the polygon to "fall" down out of the graphics window

    for i in range(2000):

        p.move(0,800/2000)

# Define highscore() function. It accepts no arguments and returns no values

def highscore():

    # Open and read scores.txt file into variable data

    infile = open("scores.txt","r")
    data = infile.readlines()
    infile.close()

    # Initialize variables

    top7 = []
    top7objects = []
    increasing = 55

    # While there are less than 7 top scores:

    while len(top7) < 7:

        # Initialize variables

        highest = 0
        index = 0

        # For every line in data:

        for i in enumerate(data):

            # Process the line

            x = i[1].replace("\n","")
            x = x.split(",")

            # Find the top score
            
            if int(x[2]) > highest:
            
                highest = int(x[2])
                index = i[0]

        # Add the top score to the top7 list

        top7.append((data[index].replace("\n","")).split(","))

        # Remove the top score from data

        del data[index]

    # Create graphics objects

    window = GraphWin("High Scores",350,190)
    window.setBackground("white")

    header1 = Text(Point(175,15),"Player              Rounds  Score")
    header1.setFace("courier")
    header1.setStyle("bold")
    header1.draw(window)
    top7objects.append(header1)
    header2 = Text(Point(175,35),"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    header2.setFace("courier")
    header2.setStyle("bold")
    header2.draw(window)
    top7objects.append(header2)

    # Create a formatted text object for every score in top7

    for i in range(7):
        
        text = Text(Point(175,increasing),"{0:<19}{1:^8}{2:>6}".format(top7[i][0],top7[i][1],top7[i][2]))
        text.setFace("courier")
        text.setStyle("bold")
        text.draw(window)
        top7objects.append(text)

        increasing += 20

    # Create an infinite loop that animates the text objects and that is stopped when a click is registered inside the window

    while True:

        try:
            if window == None:

                break

            click = window.checkMouse()

            if click != None:

                break

            for i in top7objects:

                i.move(0,-1/30)

                if (i.getAnchor()).getY() <= -5:

                    i.move(0,200)

        except GraphicsError:
            
            break

    # Close the window
    
    window.close()
    
# Call main()

main()
