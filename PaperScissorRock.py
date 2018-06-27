import random
import string
import time


class PaperScissorRock:
    def __init__(self):
        self.user_name = "player"
        self.comp_score = 0
        self.human_score = 0
        self.comp_weapon = "paper"
        self.human_weapon = "paper"
        self.top_message = ''
        self.foot_message = ''

    def user_name_input(self):

        valid = string.ascii_letters + " "  # a space is include for name with spaces inside say 'Peter Paul Mary'

        while True:
            name = input('\n\n\nPlease enter your name:   ')
            if name == '':
                break
            elif set(name).issubset(valid):
                self.user_name = name
                welcome_message = (f"\nHello {self.user_name}, welcome to this game.\n",
                                   f"There are three weapons you can use.\n",
                                   f"Paper (p) to win Rock (r) which win scissor (s) and scissor win Paper \n",
                                   f"Entering 'r', 's', or 'p' to fight the computer\n",
                                   f"you can quit at any time after the fight by entering 'q'\n",
                                   f"or just press 'enter' for the next fight")
                for message in welcome_message:
                    print(message)
                    time.sleep(2)
                time.sleep(3)
                print('So, lets fight')
                time.sleep(2)
                break
            else:
                print('please enter valid name')

    def gen_comp_weapon(self):
        w_dict = {"r": 'rock', "p": 'paper', 's': 'scissor'}
        rand_string = "rsprsrprrrsrrpprsrsrrrsprrssrsspspspprsprsrssrsssrprrprppppssrrssrrpprss"
        self.comp_weapon = w_dict[random.choice(rand_string)]

    def display(self, clear=False):
        weapons_dict = {"scissor": "✂", "paper": "👋", "rock": "✊"}
        if clear:
            comp_weapon_img = ""
            human_weapon_img = ""
            comp_weapon = ""
            human_weapon = ""
        else:
            comp_weapon_img = weapons_dict[self.comp_weapon]
            human_weapon_img = weapons_dict[self.human_weapon]

            comp_weapon = self.comp_weapon
            human_weapon = self.human_weapon
        print("\n" * 10)
        print(f"\t\t{self.top_message}")
        print()
        print("\t\t\t\t===============================")
        print("\t\t\t\t          ＳＣＯＲＥ")
        print("\t\t\t\t===============================")
        print(f"\t\t\t\t     {self.comp_score}      |        {self.human_score}")
        print("\t\t\t\t===============================")
        print(f" \t\t\t\t Computer          {self.user_name}")
        print("\t\t\t\t-------------------------------")
        print("\t\t\t\t             |  ")
        print(f"\t\t\t\t     {comp_weapon_img}              {human_weapon_img} ")
        print("\t\t\t\t             |  ")
        print("\t\t\t\t-------------------------------")
        print(f"\t\t\t\t    {comp_weapon}        {human_weapon}")
        print("\t\t\t\t-------------------------------")
        print(f"\t\t\t\t         {self.foot_message}")
        print("\n\n\n\n")

    def game(self):
        random.seed(time.time())
        self.user_name_input()
        while True:

            self.user_input()
            self.gen_comp_weapon()
            who_win = self.who_win()
            if who_win == "human":
                self.human_score += 1
                self.foot_message = f"{self.user_name} win"
            elif who_win == "computer":
                self.comp_score += 1
                self.foot_message = "computer win"
            else:
                self.foot_message = "this is a draw"
            self.top_message = "enter 'q' if want to quit or 'enter' to continue"
            self.display()
            again = input('::')
            if again.lower() == 'q' or again.lower() == 'Q':
                break

    def user_input(self):
        VALIDLIST = "rsp"
        w_dict = {"r": 'rock', "p": 'paper', 's': 'scissor'}
        while True:

            self.top_message = "Please enter you choice of weapon: 'r' for rock, 'p' for paper or 's' for scissor"
            self.foot_message = ""
            self.display(clear=True)
            weapon = input("::")
            weapon = weapon.lower()
            if len(weapon) == 1 and set(weapon).issubset(VALIDLIST):
                self.human_weapon = w_dict[weapon]
                break
            else:
                self.message = f"{self.user_name} , Please enter either 'r','s' or 'p' "

    def who_win(self):
        win_dict = {"scissor": "paper", "paper": "rock", "rock": "scissor"}
        if self.human_weapon == self.comp_weapon:
            return "draw"
        if win_dict[self.human_weapon] == self.comp_weapon:
            return "human"
        return "computer"


def main():
    paper = PaperScissorRock()
    paper.game()


main()

