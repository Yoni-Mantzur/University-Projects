package ex1;

import java.util.Scanner;
/**
 * The Competition class represents a Nim competition between two players, 
 * consisting of a given number of rounds. 
 * It also keeps track of the number of victories of each player.
 * @author Yoni Mantzur and OOP staff
 * @see Move
 * @see Compitition
 * @see Player
 */
public class Competition {
	
	private static final int PLAYER1 = 1, PLAYER2 = 2;
	private static final int HUMAN = 4;
	private static final Object INVALID_MOVE = null;
		
	private Player player1, player2;
	private boolean displayMessage;
	private int victoriesPlayer1;
	private int victoriesPlayer2;

	
	/**
	 * Constructor.
	 * @param player1 - The first player to play in game (1-4).
	 * @param player2 - The second player to play in game (1-4). 
	 * @param displayMessage - True if to show messages over the game(depends
	 * if human player is in).
	 */
	public Competition(Player player1, Player player2,
									boolean displayMessage){
		
		this.player1 = player1;
		this.player2 = player2;
		this.displayMessage = displayMessage;
		this.victoriesPlayer1 = 0; // Counter of the score each round each player
		this.victoriesPlayer2 = 0;

		}
	
	/*
	 * Returns the integer representing the type of the player; returns -1 on bad
	 * input.
	 */
	private static int parsePlayerType(String[] args,int index){
		try{
			return Integer.parseInt(args[index]);
		} catch (Exception E){
			return -1;
		}
	}
	
	/*
	 * Returns the integer representing the type of player 2; returns -1 on bad
	 * input.
	 */
	private static int parseNumberOfGames(String[] args){
		try{
			return Integer.parseInt(args[2]);
		} catch (Exception E){
			return -1;
		}
	}
	
	
	/**
	 * Run the game for the given number of rounds.
	 * @param numberOfRounds - The number of rounds to play.
	 */
	public void playMultipleRounds(int numberOfRounds){
				
		for (int round=1; round<=numberOfRounds; round++){
		
			singleRound(); // runs single rounds each iteration.
		}
		
		System.out.printf("The results are %d:%d%n", this.victoriesPlayer1,
												this.victoriesPlayer2);
	}
	
	/*
	 * Update the victories regard the winner.
	 * Effect: the score of each player will change regard to the round.
	 */
	private void upDateVictories(Player playerWon){
		
		
		if (playerWon.equals(this.player1)){
			this.victoriesPlayer1++;
		} else {
			this.victoriesPlayer2++;
		}
		
	}
	
	/*
	 * Runs one round of the game.
	 */
	private void singleRound(){
		
		boolean notInvalidMove = true; // Charge on the message in first move 
		Board board = new Board();
		Player currentPlayer = this.player1; // Player1 always start first!
		
		if (this.displayMessage){
			System.out.println("Welcome to the sticks game!");

		}
		while (board.getNumberOfUnmarkedSticks() > 0){
			
			if (this.displayMessage && notInvalidMove){
				System.out.printf("Player %d, it is now your turn!%n", 
					currentPlayer.getPlayerId());
				notInvalidMove = false;
			}
			// The player take a move
			Move turnPlayer = singleTurn(currentPlayer, board);
			
			if (this.displayMessage){
						
				if (turnPlayer == INVALID_MOVE){ 
					System.out.println("Invalid move. Enter another:");
					continue;
				}
			
				System.out.printf("Player %d made the move: " + turnPlayer + "\n",
										currentPlayer.getPlayerId());
				
			} else if (turnPlayer == INVALID_MOVE){ // Check valid move with no massages
				continue;
			}
			
			currentPlayer = nextPlayerTurn(currentPlayer);
			notInvalidMove = true;
		}
		
		if (this.displayMessage){
			System.out.printf("Player %d won!%n", currentPlayer.getPlayerId());
		}
		
		upDateVictories(currentPlayer);
	}
	
	/*
	 * Charge of movement of player in the game in his turn.
	 * playerTurn; The player his turn to pick a move.
	 * currentBoard; The board before the move of the player
	 * Effects: the board will be change regard to the move.
	 */
	private Move singleTurn(Player playerTurn, Board currentBoard){
		
		final int MOVE_LEGAL = 1; // Means the move is legal
		
		Move move = playerTurn.produceMove(currentBoard); // The player marked 
		
		if (currentBoard.markStickSequence(move) != MOVE_LEGAL){	
			
					return null; //Invalid move.			
		}	
		
		return move;
	}
	
	/*
	 * Check of who is next turn to be in the game.
	 * currentPlayerId; The player his played at this movement.
	 * return the current player to play
	 */
	private Player nextPlayerTurn(Player currentPlayer){
		
		if (currentPlayer.getPlayerId() == this.player1.getPlayerId()){
			
			currentPlayer = this.player2;
		} else {
			currentPlayer = this.player1;
		}
		
		return currentPlayer;	
	}
	
	/**
	 * Tells the score of requested opponent in the current moment.
	 * @param playerPosition - means 1 - player1, 2 - player2.
	 * @return The number of rounds the player wins.
	 */
	public int getPlayerScore(int playerPosition){
		
		switch(playerPosition){
			
			case PLAYER1:
				return this.victoriesPlayer1;
				
			case PLAYER2:
				return this.victoriesPlayer2;
				
			default: // If get here means send illegal position
				return -1;
		
		}
	}
	
	/**
	 * The method runs a Nim competition between two players according to the 
	 * three user-specified arguments. 
	 * (1) The type of the first player, which is a positive integer between 
	 * 1 and 4: 1 for a Random computer player, 2 for a Heuristic 
	 * computer player, 3 for a Smart computer player and 4 for a human player.
	 * (2) The type of the second player, which is a positive integer between 
	 * 1 and 4.
	 * (3) The number of rounds to be played in the competition.
	 * @param args - an array of string representations of the three input 
	 * arguments, as detailed above.
	 */
	public static void main(String[] args) {
		
		int p1Type = parsePlayerType(args,0);
		int p2Type = parsePlayerType(args,1);
		int numGames = parseNumberOfGames(args);

		boolean flagMassages;
		Scanner scanner = new Scanner(System.in);
		
		// Second argument is the Id of the player.
		Player player1 = new Player(p1Type, PLAYER1, scanner);
		Player player2 = new Player(p2Type, PLAYER2, scanner);
		
		System.out.printf("Starting a Nim competition of %d rounds between a " +player1.getTypeName()
				+" player" + " and a "+player2.getTypeName()+" player.%n", numGames);
		
		if (p1Type == HUMAN || p2Type == HUMAN){
			flagMassages = true;
		} else {
			flagMassages = false;
		}
		
		Competition competition = new Competition(player1,player2,flagMassages);
		competition.playMultipleRounds(numGames); // runs the game


	}// end Main
	
} // end Class
