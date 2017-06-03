package orders;

import java.io.File;

/**
 * Represent a type order regard to the type of the file as implements Comparator interface.
 * @author YONI
 *
 */
public class TypeOrder implements Order {
	/** Name of the Order */
	public static final String ORDER_NAME = "type";
	/* Represent the start of suffix in name */
	private final static char START_SUFFIX = '.';

	private final static int EQUALS_SUFFIX = 0;
	
	/* The class will be a singleton */
	private static final Order TYPE_ORDER_SINGLTON = new SizeOrder();
	
	/* No need of other instance of this class */
	private TypeOrder() {}
	
	/**
	 * @return an instance of this class.
	 */
	public static Order instanceSizeOrder(){
		
		return TYPE_ORDER_SINGLTON;
		
	}
	
	/*
	 * Return the suffix of name of the file given.
	 */
	private String findSuffix(File file){
		
		String nameFile = file.getName();
		
		int indexStartSuffix = nameFile.lastIndexOf(START_SUFFIX) + 1;
		
		return nameFile.substring(indexStartSuffix, nameFile.length() -1);
		
	}

	/**
	 * Compare by the type of the files, (If equals with absOrder).
	 * 
	 * @param file1 - file to compare.
	 * @param file1 - file to compare.
	 * @return 1 for file1 bigger, 0 for equals and -1 for smaller
	 */
	@Override
	public int compare(File file1, File file2) {
		
		int comparing = findSuffix(file1).compareTo(findSuffix(file2));
		
		// If equals return the absOrder result.
		if (comparing == EQUALS_SUFFIX)
			comparing = AbsOrder.instanceAbsOrder().compare(file1, file2);
		
		return comparing;
	}

}
