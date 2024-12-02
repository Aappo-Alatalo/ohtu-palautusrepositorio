class TennisGame:

    CALLS = ["Love", "Fifteen", "Thirty", "Forty"]
    WINNING_THRESHOLD = 4

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_scores = {
            player1_name: 0,
            player2_name: 0
        }

    def won_point(self, player_name):
        self.m_scores[player_name] += 1

    def is_tied(self):
        return self.m_scores[self.player1_name] == self.m_scores[self.player2_name]
    
    def get_tied_score(self):
        score = self.m_scores[self.player1_name]
        return f"{self.CALLS[score]}-All" if score < 3 else "Deuce"
    
    def has_advantage_or_win(self):
        return any(score >= self.WINNING_THRESHOLD for score in self.m_scores.values())
    
    def get_advantage_or_win_score(self):
        diff = self.m_scores[self.player1_name] - self.m_scores[self.player2_name]
        if diff == 1:
            return f"Advantage {self.player1_name}"
        elif diff == -1:
            return f"Advantage {self.player2_name}"
        elif diff >= 2:
            return f"Win for {self.player1_name}"
        else:
            return f"Win for {self.player2_name}"
    
    def get_regular_score(self):
        player1_score = self.CALLS[self.m_scores[self.player1_name]]
        player2_score = self.CALLS[self.m_scores[self.player2_name]]
        return f"{player1_score}-{player2_score}"

    def get_score(self):
        if self.is_tied():
            return self.get_tied_score()
        elif self.has_advantage_or_win():
            return self.get_advantage_or_win_score()
        else:
            return self.get_regular_score()
