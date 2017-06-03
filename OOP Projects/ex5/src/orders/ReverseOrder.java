package orders;

import java.io.File;


/**
 * Represent an opposite order regard to some order chosen, implements Comparator interface.
 * @author YONI
 *
 */
class ReverseOrder implements Order {

	/** Name of the Order */
	public static final String ORDER_NAME = "REVERSE";
	
	/* Represent the filter to negative */
	private final Order ORDER_TO_REVERSE;
	
	/**
	 * Constructor.
	 * @param orderToReverse - The order to reverse
	 * @throws OrderException - the order to reverse is null.
	 */
	public ReverseOrder(Order orderToReverse) throws OrderException {
		
		if (orderToReverse == null)
			throw new OrderException();
		
		ORDER_TO_REVERSE = orderToReverse;
		
	}

	/**
	 * Compare by some order by in the reverse.
	 * 
	 * @param file1 - file to compare.
	 * @param file1 - file to compare.
	 * @return 1 for file1 bigger, 0 for equals and -1 for smaller
	 */
	@Override
	public int compare(File file1, File file2) {

		// return the opposite of the source order.
		return -ORDER_TO_REVERSE.compare(file1, file2);
	}

}
