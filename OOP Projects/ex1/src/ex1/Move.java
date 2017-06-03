package ex1;


/**
 * Represents a move done by the player in the 'Nim' game, means what sticks 
 * he marked.
 * @author Yoni Mantzur
 * @see Board
 * @see Compitition
 * @see Player
 */
public class Move {
	
	private int inRow, inLeft, inRight;
	
	/**
	 * Constructor.
	 * @param inRow - The number of row the player marked.
	 * @param inLeft - The number of left bound the player marked. 
	 * @param inRight - The number of right bound the player marked.
	 */
	public Move(int inRow, int inLeft, int inRight){
		
		this.inRow = inRow;
		this.inLeft = inLeft;
		this.inRight = inRight;
		
	}
	
	/**
	 * Representation of a move done by player.
	 * @return the representation of a move.
	 */
	public java.lang.String toString(){
		
		return (this.inRow + ":" + this.inLeft + "-" + this.inRight);
	}
	
	/**
	 * Number of row the player marked
	 * @return the row the player marked.
	 */
	public int getRow(){
		
		return this.inRow;
		
	}
	
	/**
	 * Number of left bound the player marked.
	 * @return the left bound the player marked.
	 */
	public int getLeftBound(){
		
		return this.inLeft;
		
	}
	
	/**
	 * Number of right bound the player marked.
	 * @return the right bound the player marked.
	 */
	public int getRightBound(){
		
		return this.inRight;
	}

}
