package ex1;

/**
 * The Board class represents a board of the Nim game. 
 * The board can be of a variable size. In this implementation 
 * it only has 4 rows, 7 sticks in the first row, and 5,3 and 1 sticks
 *  in the following rows. A board object is 
 * disposable, meaning that the moves performed on the board are not 
 * reversible, and if a "clean" board is required, 
 * the user has to initialize a new board object.
 * @author OOP course staff
 */
public class Board {

	/** The template of a Nim game board. */
	private static final int[][] boardTemplate = 
								{{1,1,1,1,1,1,1},{1,1,1,1,1},{1,1,1},{1}};
	/** The number of rows in a Nim game board. */
	private static final int NUM_OF_ROWS = boardTemplate.length;
	/** The maximal number of sticks in a single row in a Nim game board. */
	private static final int MAX_NUM_OF_STICKS_IN_ROW = 
													boardTemplate[0].length;
	/** The total number of sticks in a Nim game board. */
	private static final int NUM_OF_ELEMENTS = 
								NUM_OF_ROWS*(1+MAX_NUM_OF_STICKS_IN_ROW)/2;	
	
	private int[][] gameBoard; //2d array representing the game board.
	private int numberOfMarkedSticks; //Number of currently marked sticks 
									  //on the board.
	
	
	/**
	 * Initializes a clear board.
	 */
	public Board(){		
		numberOfMarkedSticks = 0;
		gameBoard = new int[NUM_OF_ROWS][];
		// Remember: when we have only one line inside a for/while loop,
		// we do not have to use curly brackets! See below:
		for(int i = 0; i < NUM_OF_ROWS; i++)
			gameBoard[i] = (int[]) boardTemplate[i].clone();		
	}
	
	/**
	 * Returns a multi-line human-readable visual representation of the board 
	 * as a String object. Can be used for printing the board to screen and for
	 * debugging.
	 */
	public String toString(){
		/*
		 * When we implement a public method named 'toString()' (exactly 
		 * this name!) which returns a String for some class, then when we 
		 * send an object of this class to methods like
		 * System.out.print() or println(), they will print this output String. 
		 * If the object has no such method, print() and println() will 
		 * print using the template class_name@hashCodeIdentifier,
		 * which in this case will look something like oop.ex1.Board@55f96302
		 */
		String output = "";
		int currentLength,i,j;
		for(i = NUM_OF_ROWS-1 ; i>=0 ; i--){
			
			currentLength = gameBoard[i].length;
			for(j=0;j<(MAX_NUM_OF_STICKS_IN_ROW-currentLength)/2.0;j++)
				output += " ";
			
			for(j=0;j<currentLength;j++)
				output += gameBoard[i][j];
			
			for(j=0;j<(MAX_NUM_OF_STICKS_IN_ROW-currentLength)/2.0;j++)
				output += " ";
			
			output += '\n';	
		}
		
		return output;
	}
	
	/**
	 * Makes an attempt to mark the given stick sequence on the board.
	 * In case the move is illegal the board is not changed and an appropriate 
	 * error code is returned:
	 * If the given coordinates exceed the boundaries of the board, -1 
	 * is returned. 
	 * If the current move overlaps with previously marked sticks, 0 is
	 *  returned.
	 * If the move is legal, the board changes accordingly, the number of
	 *  marked sticks in the "numMarked" is updated,
	 * 1 is returned.
	 * @param move the move to perform
	 * @return 1 if the move was legal, 0 and -1 if the move is not legal 
	 * (details above).
	 */
	public int markStickSequence(Move move){
		
		int rowNumber,leftBound,rightBound;
		rowNumber = move.getRow();
		leftBound = move.getLeftBound();
		rightBound = move.getRightBound();
		
		// Checking for legal bounds of the move
		if( (leftBound < 1) || (leftBound > rightBound) || rowNumber <1 
				|| rowNumber>NUM_OF_ROWS 
							|| (rightBound>gameBoard[rowNumber-1].length) )
			return -1;
		
		// Checking for moves covering already-marked sticks
		for(int j=leftBound-1;j<rightBound;j++){
			if(gameBoard[rowNumber-1][j] == 1)
				gameBoard[rowNumber-1][j] = 0;
			else{ //Illegal move,revert back and return error.
				for(int back=j-1;back>=leftBound-1;back--){
					gameBoard[rowNumber-1][back] = 1;
				}
				return 0;
			}
		}
		
		numberOfMarkedSticks += (rightBound-leftBound+1);
		
		return 1;
	}
	
	
	/**
	 * Returns the number of rows in the board
	 */
	public int getNumberOfRows(){
		return NUM_OF_ROWS;
	}
	
	/**
	 * Returns the total number of sticks (marked and unmarked) in the row. 
	 * A legal input to this method is an integer number between 1 and the
	 * output of "getNumberOfRows()". Returns -1 in case the input is invalid.
	 */
	public int getRowLength(int row){
		
		if(row<1 || row>NUM_OF_ROWS)
			return -1;
		
		return gameBoard[row-1].length;
	}
	
	/**
	 * Given an index to the stick position (row and number in row - 
	 * counting from the left side), this method returns true if the stick is
	 * unmarked, and false if it is marked, or if the input is out of bounds. 
	 */
	public boolean isStickUnmarked(int row,int stickNum){
		
		if(row<1 || row>NUM_OF_ROWS || stickNum<1 
									|| stickNum>gameBoard[row-1].length)
			return false;
		
		return(gameBoard[row-1][stickNum-1]==1);
		
	}
	
	/**
	 * @return The number of marked sticks on the board.
	 */
	public int getNumberOfMarkedSticks() {
		// This is a classic "getter" method. We use getter methods when we 
		// want other classes to be able to read the value of some private 
		// field in some class, without being able to change it.
		// If we simply made the field (in this case 'numMarked') public, 
		// other classes could read AND change it, so this is a better solution
		return numberOfMarkedSticks;
	}
	
	/**
	 * @return the number of unmarked sticks on the board.
	 */
	public int getNumberOfUnmarkedSticks(){
		return NUM_OF_ELEMENTS - numberOfMarkedSticks;
	}
	
	
}
