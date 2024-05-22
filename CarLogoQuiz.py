import tkinter as tk
import random
from threading import *
from tkinter import messagebox
from pygame import mixer
import carBrandLogoImages as cb

class CarLogoQuiz:
    score = 0
    shuffled = []
    brandNameNow = ""
    def __init__(self):
        self.window = tk.Tk()
        # Dimension of the GUI window
        self.window.geometry("1200x800")
        self.window.minsize(width=1200, height=800)
        # Title on the title bar of the GUI window
        self.window.title("Car Logo Quiz")
        # Setting the background color of master container 'window' to pale cream yellow color.
        self.window.config(bg="#f9faaf")
        self.buttonSelected = 0
        # icons are converted to PhotoImage
        self.coins = tk.PhotoImage(file="assets/images/ui/coins.png")
        self.nextButtonIcon = tk.PhotoImage(file="assets/images/ui/next-50.png")
        self.carLogoQuizPhoto = tk.PhotoImage(file="assets/images/ui/carlogoquiz_icon.png")
        # brand names list
        self.brandNamesList = ["Audi", "Lamborghini", "Ferrari", "Mercedes", "Rolls Royce", "Hyundai", "Honda", "BMW", "Bentley", "Bugatti",
                               "Yamaha", "Suzuki", "Aston Martin", "Acura", "Ford", "BYD", "Cadillac", "Chevrolet", "Citroen", "Fiat",
                               "Renault", "Kia", "Jeep", "Land Rover", "Lexus", "Maserati", "Lincoln", "Volvo", "Mazda", "Nissan", "Peugeot",
                               "Pontiac", "Porsche", "Tesla", "Maybach", "Mahindra", "Volkswagen", "Apollo Automobil", "Ligier", "Subaru",
                               "Mitsubishi","Toyota","Alfa","Opel","Skoda","Chrysler","McLaren","Saab","Lotus","General Motors",
                               "Buick","Koenigsegg","Dacia","Geely","Rossion","Dodge"]
        # Copy of list 'brandNamesList' to help in creating choice buttons randomly
        self.copyBrandNamesList = self.brandNamesList.copy()
        # dictionary. Elements of dictionary in same order as in brandNamesList mapping to its PhotoImage variable.
        self.logoBrandnameMap = {"Audi":cb.loadAudi(),"Lamborghini":cb.loadLamborghini(),
                    "Ferrari": cb.load_ferrari(), "Mercedes": cb.load_mercedes(),"Rolls Royce": cb.load_rolls_royce(),
                                 "Hyundai": cb.load_hyundai(), "Honda": cb.load_honda(), "BMW": cb.load_bmw(),
                                 "Bentley": cb.load_bentley(), "Bugatti": cb.load_bugatti(),
                                 "Yamaha": cb.load_yamaha(),
                                 "Suzuki": cb.load_suzuki(), "Aston Martin": cb.load_astonmartin(),
                                 "Acura": cb.load_acura(), "Ford": cb.load_ford(), "BYD": cb.load_byd(),
                                 "Cadillac": cb.load_cadillac(),
                                 "Chevrolet": cb.load_chevrolet(), "Citroen": cb.load_citroen(), "Fiat": cb.load_fiat(),
                                 "Renault": cb.load_renault(), "Kia":cb.load_kia(), "Jeep":cb.load_jeep(),
                                 "Land Rover": cb.load_landrover(),
                                 "Lexus": cb.load_lexus(), "Maserati": cb.load_maserati(), "Lincoln": cb.load_lincoln(),
                                 "Volvo": cb.load_volvo(), "Mazda": cb.load_mazda(), "Nissan": cb.load_nissan(),
                                 "Peugeot":cb.load_peugeot(),
                                 "Pontiac": cb.load_pontiac(), "Porsche": cb.load_porsche(), "Tesla": cb.load_tesla(),
                                 "Maybach": cb.load_maybach(), "Mahindra": cb.load_mahindra(), "Volkswagen": cb.load_volkswagen(),
                                 "Apollo Automobil": cb.load_apollo_automobil(), "Ligier": cb.load_ligier(),
                                 "Subaru": cb.load_subaru(),"Mitsubishi": cb.load_mitsubishi(),
                                 "Toyota":cb.load_toyota(),"Alfa":cb.load_alfa(),"Opel":cb.load_opel(),"Skoda":cb.load_skoda(),
                                 "Chrysler":cb.load_chrysler(),"McLaren":cb.load_mclaren(),"Saab":cb.load_saab(),
                                 "Lotus":cb.load_lotus(),"General Motors":cb.load_general_motors(),"Buick":cb.load_buick(),
                                 "Koenigsegg":cb.load_koenigsegg(),"Dacia":cb.load_dacia(),"Geely":cb.load_geely(),
                                 "Rossion":cb.load_rossion(),"Dodge":cb.load_dodge()}
        # Create a frame 'frame1' which hold three frames in it.
        self.frame1 = tk.Frame(self.window,bg="#f9faaf")
        self.frame1.pack(pady=40)
        # frame 'frameLeft' created with its master 'frame1'
        self.frameLeft = tk.Frame(self.frame1,bg="#f9faaf")
        self.frameLeft.grid(row=0,column=0)
        # frame 'frameCenter' created with its master 'frame1'
        self.frameCenter = tk.Frame(self.frame1,bg="#f9faaf")
        self.frameCenter.grid(row=0,column=1)
        # frame 'frameTv' created with its master 'frameCenter'.
        # This 'frameTv' contains the canvas inside it to display logos.
        self.frameTv = tk.Frame(self.frameCenter,bg="black")
        self.frameTv.pack()
        # frame 'frameRight' created with its master as 'frame1'.
        self.frameRight = tk.Frame(self.frame1,bg="#f9faaf")
        self.frameRight.grid(row=0, column=2)
        # canvas with width 200 and height 200 created with its master 'frameTv'.
        self.imageDisplay = tk.Canvas(self.frameTv,height=200,width=200,bg="white")
        # The canvas 'imageDisplay' has padding in x-axis 6 and padding in y-axis 7
        self.imageDisplay.pack(padx=6, pady=7)
        # next button widget
        self.nextButton = tk.Button(self.frameCenter,text="Next", command=self.threading, font=("Monotype Corsiva",20), bg="#BEA4F1", cursor="heart",image=self.nextButtonIcon,compound=tk.LEFT,padx=10)
        self.nextButton.pack(side=tk.BOTTOM)
        # exit button
        self.exitButton = tk.Button(self.frameRight, text="EXIT GAME", command=self.quit_game, bg="red", fg="black",relief=tk.RAISED,bd=5,font=("Helvetica",14))
        self.exitButton.pack(padx=40)
        # score displaying Label
        self.scoreLabel = tk.Label(self.frameLeft,text="Score:0 ", font=("Helvetica",16,"bold"), compound=tk.RIGHT, image=self.coins, bg="#f9faaf",fg="blue")
        self.scoreLabel.pack(padx=60)
        # variable to display score
        self.selected = tk.IntVar()
        # frame
        self.frame = tk.Frame(self.frameCenter,bg="#f9faaf")
        self.frame.pack(pady=25)
        # button1
        self.btn1 = tk.Button(self.frame,text="A", command=self.button1,width=20,bg="skyblue",font=("Arial",17),activebackground="skyblue")
        self.btn1.grid(row=0,column=0,pady=5)
        # button 2
        self.btn2 = tk.Button(self.frame, text="B", command=self.button2,width=20,bg="skyblue",font=("Arial",17),activebackground="skyblue")
        self.btn2.grid(row=0,column=2,pady=5)
        # button 3
        self.btn3 = tk.Button(self.frame, text="C", command=self.button3,width=20,bg="skyblue",font=("Arial",17),activebackground="skyblue")
        self.btn3.grid(row=1,column=0,pady=5)
        # button 4
        self.btn4 = tk.Button(self.frame, text="D", command=self.button4,width=20,bg="skyblue",font=("Arial",17),activebackground="skyblue")
        self.btn4.grid(row=1,column=2,pady=5)
        # submit button
        self.submit = tk.Button(self.frame,text="Submit", command=self.getSelected, font=("Monotype Corsiva",20),bg="black",fg="yellow",activebackground="#3b3b36",activeforeground="white")
        self.submit.grid(row=2,column=1,pady=10)
        # Starting the canvas with first picture
        self.nextPicture()
        # setting the icon in window title bar
        self.window.iconphoto(True, self.carLogoQuizPhoto)
        self.window.mainloop()

    # Function to change next picture in canvas along with different texts on 4 buttons
    def nextPicture(self):
        global buttonSelected
        # play the clicking sound
        self.thread_play_click_sound()
        # Initially when a new brand logo is appeared on Canvas, the player has not clicked any buttons yet.
        # So the variable 'buttonSelected' is initialized to 0
        self.buttonSelected = 0
        # Reset the background color of all 4 choice buttons to skyblue
        self.changeBtn1BgColor("skyblue")
        self.changeBtn2BgColor("skyblue")
        self.changeBtn3BgColor("skyblue")
        self.changeBtn4BgColor("skyblue")
        # Reset the text color of all 4 choices buttons to black
        self.changeBtn1FgColor("black")
        self.changeBtn2FgColor("black")
        self.changeBtn3FgColor("black")
        self.changeBtn4FgColor("black")
        # Disable the Next button. Because without clicking any of the 4 button and without clicking the 'Submit' button, player cannot
        # move to the next randomly displaying logo question.
        self.disableNextButton()
        # Activate the 'Submit' button so that player can click any of the 4 choice buttons and then click 'Submit' button.
        self.normalSubmitButton()
        # Our application is developed such that a brand logo which appeared as question once, should not repeat again.
        # To perform this, the brand logo which appeared in Canvas once as question is removed from the array 'brandNamesList'.
        # Hence check if there are any more brand logos present in array 'brandNamesList'. If YES, continue to display any logo in Canvas
        # in random order. Otherwise display to player 'GAME OVER' and the player's score.
        if len(self.brandNamesList) > 0:
            global brandNameNow,shuffled
            currIndex = random.randrange(0, len(self.brandNamesList))
            currentBrand = self.brandNamesList[currIndex]
            brandNameNow = currentBrand
            self.imageDisplay.delete('all')
            self.imageDisplay.create_image(0, 0, image=self.logoBrandnameMap.get(currentBrand), anchor=tk.NW)
            # Create an array 'arr' containing 3 random brand names and 1 correct brand name of the brand logo in Canvas now.
            arr = self.createChoices(currentBrand, currIndex,self.copyBrandNamesList)
            # Change the order of elements in the array 'arr' by shuffling using random.
            self.shuffleArray(arr)
            shuffledList = arr
            shuffled = shuffledList
            # Assign the elements of shuffled array 'shuffledList' as the text of 4 choice buttons.
            self.btn1.config(text=shuffledList[0])
            self.btn2.config(text=shuffledList[1])
            self.btn3.config(text=shuffledList[2])
            self.btn4.config(text=shuffledList[3])
            # Pop the current image displayed from list 'brandNamesList' so that it wont repeat again in question
            self.brandNamesList.pop(currIndex)

        else:
            # Display to player GAME OVER with score. All Logos answered.
            self.thread_play_game_level_completed_sound()
            finalScore = f"Your SCORE is {str(self.score)}"
            messagebox.showinfo("GAME OVER",finalScore)
            self.disableChoicesButtons()
            self.disableSubmitButton()

    # Function to perform changing to next logo in Canvas 'imageDisplay' in a separate thread
    def threading(self):
        # Call work function
        t1 = Thread(target=self.nextPicture)
        t1.start()

    # Function to play the winning sound when user submits correct answer for logo
    def playAudio(self):
        mixer.init()
        mixer.music.load("assets/sound_effects/mixkit-instant-win-2021.wav")
        mixer.music.set_volume(0.8)
        mixer.music.play()

    # Function to play the clicking sound on clicking buttons in the GUI
    def play_click_sound(self):
        mixer.init()
        mixer.music.load("assets/sound_effects/mixkit-classic-click-1117.wav")
        mixer.music.set_volume(0.8)
        mixer.music.play()
    def thread_play_click_sound(self):
        thread_var = Thread(target=self.play_click_sound())
        thread_var.start()
    # Function to play the wrong answer buzzer sound
    def play_wrong_answer_sound(self):
        mixer.init()
        mixer.music.load("assets/sound_effects/mixkit-game-show-wrong-answer-buzz-950.wav")
        mixer.music.set_volume(0.8)
        mixer.music.play()
    def thread_play_wrong_answer_sound(self):
        thread_var = Thread(target=self.play_wrong_answer_sound())
        thread_var.start()
    def play_game_completed_sound(self):
        mixer.init()
        mixer.music.load("assets/sound_effects/mixkit-completion-of-a-level-2063.wav")
        mixer.music.set_volume(0.8)
        mixer.music.play()
    def thread_play_game_level_completed_sound(self):
        thread_var = Thread(target=self.play_game_completed_sound())
        thread_var.start()

    # Function to create 3 random choices in the 4 buttons when a logo appears.
    # One of the 4 random choices has correct brand passed through parameter 'brandName'
    def createChoices(self,brandName, currentIndex,copyBrandNamesList):
        choicesArr = [brandName] # Appending the correct brand name of the current logo displaying in Canvas 'imageDisplay'.
        '''Till the length of the array 'choicesArr' become 4, create 3 more random brand names from the array containing all
         the brand names 'copyBrandNamesList' except the given brandName. '''
        while len(choicesArr) < 4:
            randomIndex = random.randrange(0, len(copyBrandNamesList))
            if copyBrandNamesList[randomIndex] not in choicesArr:
                choicesArr.append(copyBrandNamesList[randomIndex])
        # Return the choicesArr containing 4 brand names including the correct brand name 'brandName'
        return choicesArr

    # Function to shuffle the given array and return it.
    # The text appearing on 4 buttons should not be always not in any order. It appears randomly.
    # Hence shuffle the given 'choicesArr' and return it.
    def shuffleArray(self,choicesArr):
        return random.shuffle(choicesArr)

    # Function to analyse the button selected by user among the 4 buttons.
    def getSelected(self):
        global buttonSelected,brandNameNow,shuffled
        self.thread_play_click_sound()
        # Index at which the correct answer given 'brandNameNow' is present in array 'shuffled' is assigned to
        # variable 'correctAnswerIndex'
        correctAnswerIndex = shuffled.index(brandNameNow)
        if self.buttonSelected!=0:
            '''Activate the Next button now because for the image displaying in the Canvas, the choice 
                    has been submitted by clicking 'Submit' button. Because of that this function is called now.'''
            self.nextButton.config(state=tk.NORMAL)
            # Disable the Submit button because the submit  button has been clicked just now.
            self.submit.config(state=tk.DISABLED)
            # If player clicked correct answer
            if shuffled[self.buttonSelected-1]==brandNameNow:
                # Increment the score of player
                self.score += 1
                # Play winning sound by creating a new separate thread
                audio_thread = Thread(target=self.playAudio)
                audio_thread.start()
            else:
                # If player clicked WRONG button as answer.
                self.thread_play_wrong_answer_sound()
                # Find the index of the wrong button selected by player. Assign it as 'wrongAnswerIndex'.
                wrongAnswerIndex = self.buttonSelected-1
                # Change the background color of the wrong button clicked by player to red.
                # If the 'wrongAnswerIndex' is 0, player clicked btn1. Change its background color to red, text color to white.
                # If the 'wrongAnswerIndex' is 1, player clicked btn2. Change its background color to red, text color to white.
                # If the 'wrongAnswerIndex' is 2, player clicked btn3. Change its background color to red, text color to white.
                # If the 'wrongAnswerIndex' is 3, player clicked btn4. Change its background color to red., text color to white.
                if wrongAnswerIndex == 0:
                    self.changeBtn1BgColor("red")
                    self.changeBtn1FgColor("white")
                elif wrongAnswerIndex == 1:
                    self.changeBtn2BgColor("red")
                    self.changeBtn2FgColor("white")
                elif wrongAnswerIndex == 2:
                    self.changeBtn3BgColor("red")
                    self.changeBtn3FgColor("white")
                elif wrongAnswerIndex == 3:
                    self.changeBtn4BgColor("red")
                    self.changeBtn4FgColor("white")
            # Display the button having the correct answer by changing that button's background color to GREEN hex color '#51f01d'.
            # If the correctAnswerIndex is 0, the button 'btn1' is having the correct answer.
            # If the correctAnswerIndex is 1, the button 'btn2' is having the correct answer.
            # If the correctAnswerIndex is 2, the button 'btn3' is having the correct answer.
            # If the correctAnswerIndex is 3, the button 'btn4' is having the correct answer.
            if correctAnswerIndex==0:
                self.changeBtn1BgColor("#51f01d")
            elif correctAnswerIndex==1:
                self.changeBtn2BgColor("#51f01d")
            elif correctAnswerIndex==2:
                self.changeBtn3BgColor("#51f01d")
            elif correctAnswerIndex==3:
                self.changeBtn4BgColor("#51f01d")
            # Update the latest score of player in the Label 'scoreLabel'
            ans = "Score:"+str(self.score)+" "
            self.scoreLabel.config(text=ans)
        else:
            messagebox.showinfo("Select","Choose any answer before submitting")

    # Function to perform event when button 'btn1' is clicked
    def button1(self):
        global buttonSelected
        self.thread_play_click_sound()
        # change the value of variable 'buttonSelected' to 1 indicating player recently clicked button 'btn1'.
        self.buttonSelected = 1

    # Function to perform event when button 'btn2' is clicked
    def button2(self):
        global buttonSelected
        self.thread_play_click_sound()
        # change the value of variable 'buttonSelected' to 2 indicating player recently clicked button 'btn2'.
        self.buttonSelected = 2

    # Function to perform event when button 'btn3' is clicked
    def button3(self):
        global buttonSelected
        self.thread_play_click_sound()
        # change the value of variable 'buttonSelected' to 3 indicating player recently clicked button 'btn3'.
        self.buttonSelected = 3

    # Function to perform event when button 'btn4' is clicked
    def button4(self):
        global buttonSelected
        self.thread_play_click_sound()
        # change the value of variable 'buttonSelected' to 4 indicating player recently clicked button 'btn4'.
        self.buttonSelected = 4

    # Function to change the state of Next button to DISABLED
    def disableNextButton(self):
        self.nextButton.config(state=tk.DISABLED)

    # Function to change the state of Submit button to DISABLED
    def disableSubmitButton(self):
        self.submit.config(state=tk.DISABLED)

    # Function to change the state of Next button to NORMAL
    def normalNextButton(self):
        self.nextButton.config(state=tk.NORMAL)

    # Function to change the state of Submit button to NORMAL
    def normalSubmitButton(self):
        self.submit.config(state=tk.NORMAL)

    # Function to change the state of the 4 choices buttons 'btn1', 'btn2', 'btn3' and 'btn4' to DISABLED
    def disableChoicesButtons(self):
        self.btn1.config(state=tk.DISABLED)
        self.btn2.config(state=tk.DISABLED)
        self.btn3.config(state=tk.DISABLED)
        self.btn4.config(state=tk.DISABLED)

    # Function to change the background color of button 'btn1' by given color variable 'colorName'.
    def changeBtn1BgColor(self,colorName):
        self.btn1.config(bg=colorName)

    # Function to change the background color of button 'btn2' by given color variable 'colorName'.
    def changeBtn2BgColor(self,colorName):
        self.btn2.config(bg=colorName)

    # Function to change the background color of button 'btn3' by given color variable 'colorName'.
    def changeBtn3BgColor(self,colorName):
        self.btn3.config(bg=colorName)

    # Function to change the background color of button 'btn4' by given color variable 'colorName'.
    def changeBtn4BgColor(self,colorName):
        self.btn4.config(bg=colorName)

    # Function to change the foreground color of button 'btn1' by given color variable 'colorName'.
    def changeBtn1FgColor(self,colorName):
        self.btn1.config(fg=colorName)

    # Function to change the foreground color of button 'btn2' by given color variable 'colorName'.
    def changeBtn2FgColor(self,colorName):
        self.btn2.config(fg=colorName)

    # Function to change the foreground color of button 'btn3' by given color variable 'colorName'.
    def changeBtn3FgColor(self,colorName):
        self.btn3.config(fg=colorName)

    # Function to change the foreground color of button 'btn4' by given color variable 'colorName'.
    def changeBtn4FgColor(self,colorName):
        self.btn4.config(fg=colorName)

    def quit_game(self):
        self.thread_play_click_sound()
        if messagebox.askyesno("Quit Game?","Do you really want to quit the game?")==True:
            self.window.destroy()

# Object created for class 'LogoQuiz'
CarLogoQuiz()