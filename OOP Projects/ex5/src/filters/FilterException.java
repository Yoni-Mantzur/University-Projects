package filters;

import oop.ex5.filescript.OneTypeException;

/**
 * Exception represent filter exceptions.
 * @author YONI
 *
 */
public class FilterException extends OneTypeException{
	
	private static final long serialVersionUID = 1L;

	/**
	 * Constructor.
	 */
	public FilterException() {
		super();
	}
	
	/**
	 * Constructor.
	 * @param message - message of the problem.
	 */
	public FilterException(String message) {
		super(message);
	}
	
}
