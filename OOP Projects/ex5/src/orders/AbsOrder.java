package orders;

import java.io.File;

/**
 * Represent an absolute order regard to the absolute path of the file as implements Comparator interface.
 * @author YONI
 *
 */
class AbsOrder implements Order {
	/** Name of the Order */
	public static final String ORDER_NAME = "abs";
	
	/* The class will be a singleton */
	private static final Order ABS_ORDER_SINGLTON = new AbsOrder();

	/* No need of other instance of this class */
	private AbsOrder() {}
	
	/**
	 * @return an instance of this class.
	 */
	public static Order instanceAbsOrder(){
		
		return ABS_ORDER_SINGLTON;
		
	}

	/**
	 * Compare by the absolute path of the files.
	 * 
	 * @param file1 - file to compare.
	 * @param file1 - file to compare.
	 * @return 1 for file1 bigger, 0 for equals and -1 for smaller
	 */
	@Override
	public int compare(File file1, File file2) {
		
		return file1.getAbsolutePath().compareTo(file2.getAbsolutePath());
	}

}