package oop.ex5.filescript;

/**
 * Exception represent second type of exceptions.
 * @author YONI
 *
 */
public class SecondTypeException extends Exception {

	private static final long serialVersionUID = 1L;
	
	/**
	 * Constructor.
	 */
	public SecondTypeException() {

		super();
	}

	/**
	 * Constructor.
	 * @param message - message of the problem.
	 */
	public SecondTypeException(String message) {
		super(message);
	}

}
