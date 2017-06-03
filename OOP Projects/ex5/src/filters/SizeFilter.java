package filters;

/**
 * Abstract Class representing Filter regarding a size of the file, implementing Filter InterFace.
 * 
 * @author YONI
 * @see BetweenFilter
 * @see GreaterThanFilter
 * @see SmallerThanFilter
 */
abstract class SizeFilter implements Filter {

	/* factor can't be negative. */
	private static final int MIN_FACTOR_SIZE = 0;
	/** The factor the filter will work to */
	protected final double FACTOR;
	
	/**
	 * Constructor.
	 * 
	 * @param factor - the factor of the size filter.
	 * @throws FilterException - if the factor not only numbers or negative.
	 */
	protected SizeFilter(String factor) throws FilterException{
		
		
			this.FACTOR = Double.parseDouble(factor);
			
			if (this.FACTOR < MIN_FACTOR_SIZE)
				throw new FilterException();
	}
		
}
