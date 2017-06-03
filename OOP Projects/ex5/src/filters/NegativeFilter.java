package filters;

import java.io.File;

/**
 * Class that represent the negative of some filter.
 * @author YONI
 *
 */
class NegativeFilter implements Filter {
	/** Filter Name */
	static final String NAME_FILTER = "NOT";
	
	/* Represent the filter to negative */
	private final Filter FILTER_NEGATIVE;
	
	/**
	 * Constructor.
	 * 
	 * @param filterToNegative - the filter to be the opposite of.
	 * @throws FilterException - the filter is null.
	 */
	public NegativeFilter(Filter filterToNegative) throws FilterException {
		
		if (filterToNegative == null)
			throw new FilterException();
		FILTER_NEGATIVE = filterToNegative;
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {

		return FILTER_NEGATIVE.filterDirectory(fileToCheack);
	}

}
