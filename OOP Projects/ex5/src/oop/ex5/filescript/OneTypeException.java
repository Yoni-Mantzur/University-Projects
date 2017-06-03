package oop.ex5.filescript;

/**
 * Exception represent one type of exceptions.
 * @author YONI
 *
 */
public class OneTypeException extends Exception {
	
	private static final long serialVersionUID = 1L;

	/**
	 * Constructor.
	 */
	public OneTypeException() {
		super();
	}

	/**
	 * Constructor.
	 * @param message - message of the problem.
	 */
	public OneTypeException(String message) {
		super(message);
		
	}

}
