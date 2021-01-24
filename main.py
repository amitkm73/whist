"""
whist score board GUI desktop app
"""
import tkinter as tk


def calc_score(round_num, bids, tricks):
    """
    :param round_num: number of rounds
    :param bids: number of tricks declared
    :param tricks: number of tricks won
    :return: score for this player in this round, note: will return 0 on illegal inputs
    """
    score = 0
    if round_num < 0 or round_num > 13 or tricks > round_num or bids < 0 or tricks < 0:
        return score
    if bids == tricks:
        if bids != 0:
            score = 10 + tricks ** 2
        else:                                   # bids == tricks == 0
            if round_num < 8:
                score = 15
            else:
                score = 30
    else:                                       # bids != tricks
        score = 8 // abs(bids-tricks)
    return score


class WhistScoreView:
    """
    tk based whist score board view
    """
    def __init__(self, master):
        """
        :param master: call this with tk root widget
        """
        self.master = master
        self.ent_player_names = []
        self.init_column_headers()
        self.init_round_numbers()
        self.spin_bids = [[], [], [], []]
        self.spin_tricks = [[], [], [], []]
        self.lbl_scores = [[], [], [], []]
        self.init_round_results()
        self.lbl_totals = []
        self.init_totals()
        self.init_button_calc()

    def init_column_headers(self):
        """ player names and bid / trick / score headers """
        col_headers = {1: "bid", 2: "tricks", 3: "score"}
        for player in range(1, 5):
            ent_player_name = tk.Entry(self.master, font='courier 10 bold', fg='blue',
                                       borderwidth=2, relief="groove")
            ent_player_name.grid(row=0, column=(player - 1) * 3 + 1, columnspan=3,
                                 sticky=tk.W + tk.E, pady=5)
            ent_player_name.insert(0, "Player" + str(player))
            self.ent_player_names.append(ent_player_name)
            for key in col_headers:
                lbl_column_header = tk.Label(self.master, text=col_headers[key],
                                             font='courier 10 bold', fg='blue',
                                             borderwidth=2, relief="groove")
                lbl_column_header.grid(row=1, column=(player - 1) * 3 + key,
                                       sticky=tk.W + tk.E, pady=2)

    def init_round_numbers(self):
        """ labels with round numbers """
        for round_num in range(1, 13):
            lbl_round_num = tk.Label(self.master, text=str(round_num), font='courier 10 bold',
                                     fg='green', pady=2)
            lbl_round_num.grid(row=round_num+1, column=0)
        row = 14
        for trump in ["C", "D", "H", "S", "NT"]:
            lbl_round_num = tk.Label(self.master, text="13"+trump, font='courier 10 bold',
                                     fg='green')
            lbl_round_num.grid(row=row, column=0)
            row += 1

    def init_round_results(self):
        """ entry widgets for bids and tricks, labels for scores """
        for player in range(0, 4):
            for round_num in range(0, 17):
                spin_bid = tk.Spinbox(self.master, from_=-1, to=min(round_num+1, 13), width=10)
                spin_bid.grid(row=round_num+2, column=player*3+1, padx=2)
                self.spin_bids[player].append(spin_bid)
                spin_trick = tk.Spinbox(self.master, from_=-1, to=min(round_num+1, 13), width=10)
                spin_trick.grid(row=round_num+2, column=player*3+2, padx=2)
                self.spin_tricks[player].append(spin_trick)
                lbl_score = tk.Label(self.master, text="0", font='courier 10 bold', fg='green',
                                     width=10, borderwidth=2, relief="groove", anchor="e")
                if round_num % 4 == player:                 # mark starting player in each round
                    spin_bid.configure(bg='LightSteelBlue2')
                    spin_trick.configure(bg='LightSteelBlue2')
                    lbl_score.configure(bg='LightSteelBlue2')
                lbl_score.grid(row=round_num+2, column=player*3+3, sticky=tk.W+tk.E, padx=2)
                self.lbl_scores[player].append(lbl_score)

    def init_totals(self):
        """ label for total score for each player """
        for player in range(0, 4):
            lbl_total = tk.Label(self.master, text="0", font='courier 10 bold', fg='red',
                                 width=10, borderwidth=2, relief="groove", anchor="e")
            lbl_total.grid(row=19, column=player*3+3, sticky=tk.W+tk.E)
            self.lbl_totals.append(lbl_total)

    def init_button_calc(self):
        """ command button that calculates scores """
        btn_calc = tk.Button(self.master, text='calculate', font='courier 10 bold',
                             fg='purple', command=self.update_scores)
        btn_calc.grid(row=20, column=1, columnspan=3, sticky=tk.W+tk.E, pady=5)

    def update_scores(self):
        """
        calculate and display scores for each valid bid x trick pair
        :return: total score of all 4 players
        """
        totals = [0, 0, 0, 0]
        for player in range(0, 4):
            for round_num in range(0, 17):
                try:
                    bid = int(self.spin_bids[player][round_num].get())
                    tricks = int(self.spin_tricks[player][round_num].get())
                except ValueError:
                    bid = -1
                    tricks = -1
                score = calc_score(min(round_num+1, 13), bid, tricks)
                self.lbl_scores[player][round_num].configure(text=str(score))
                totals[player] += score
        for player in range(0, 4):
            self.lbl_totals[player].configure(text=str(totals[player]))
        return totals[0] + totals[1] + totals[2] + totals[3]


def main():
    """
    :return: 0
    """
    root = tk.Tk()                                  # main window
    root.title("whist score board")
    whist_score_view = WhistScoreView(root)         # initialize all widgets
    print(whist_score_view.update_scores())         # just to verify all widgets are in place
    root.mainloop()
    return 0


if __name__ == '__main__':
    main()
