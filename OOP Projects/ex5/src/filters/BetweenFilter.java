package filters;
import java.io.File;

/**
 * A filter of lower and upper size of file limits
 * 
 * @author YONI
 *
 */
class BetweenFilter implements Filter{

	/** Filter Name */
	static final String NAME_FILTER = "between";
	
	/* Composing  GreaterThanFilter and SmallerThanFilter*/
	private final Filter GREATER_THAN, SMALLER_THAN;
	
	/**
	 * Constructor.
	 * 
	 * @param lowerFactor
	 * @param upperFactor
	 * @throws FilterException 
	 */
	public BetweenFilter(String lowerFactor, String upperFactor) throws FilterException{
		
		GREATER_THAN = new GreaterThanFilter(lowerFactor);
		SMALLER_THAN = new SmallerThanFilter(upperFactor);
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {

		return (GREATER_THAN.filterDirectory(fileToCheack) && SMALLER_THAN.filterDirectory(fileToCheack));
	}

}
