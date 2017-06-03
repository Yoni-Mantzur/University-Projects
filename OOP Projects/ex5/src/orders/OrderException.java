package orders;

import oop.ex5.filescript.OneTypeException;

/**
 * Exception represent order exceptions.
 * @author YONI
 *
 */
public class OrderException extends OneTypeException{
	
	private static final long serialVersionUID = 1L;

	/**
	 * Constructor.
	 */
	public OrderException() {
		super();
	}
	
	/**
	 * Constructor.
	 * @param message - message of the problem.
	 */
	public OrderException(String message) {
		super(message);
	}
	
}
