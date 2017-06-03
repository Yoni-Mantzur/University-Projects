package orders;

import java.io.File;

/**
 * Represent a size order regard to the size of the file as implements Comparator interface.
 * @author YONI
 *
 */
class SizeOrder implements Order {

	/** Name of the Order */
	public static final String ORDER_NAME = "size";
	
	private final static int EQUALS_SIZE = 0;
	
	/* The class will be a singleton */
	private static final Order SIZE_ORDER_SINGLTON = new SizeOrder();
	
	/* No need of other instance of this class */
	public SizeOrder() {}

	/**
	 * @return an instance of this class.
	 */
	public static Order instanceSizeOrder(){
		
		return SIZE_ORDER_SINGLTON;
		
	}
	
	/**
	 * Compare by the size of the files, (If equals with absOrder).
	 * 
	 * @param file1 - file to compare.
	 * @param file1 - file to compare.
	 * @return 1 for file1 bigger, 0 for equals and -1 for smaller
	 */
	@Override
	public int compare(File file1, File file2) {

		int comparing = Double.compare(file1.length(), file2.length());
		
		// If equals return the absOrder result.
		if (comparing == EQUALS_SIZE)
			comparing = AbsOrder.instanceAbsOrder().compare(file1, file1);
		
		return comparing;
	}


}
