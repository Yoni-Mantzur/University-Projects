package filters;

import java.io.File;

class GreaterThanFilter extends SizeFilter {

	/** Filter Name */
	static final String NAME_FILTER = "greater_than";
	
	/**
	 * Constructor.
	 * 
	 * @param factor - the factor of the size filter.
	 * @throws FilterException - if the factor not only numbers or negative.
	 */
	public GreaterThanFilter(String factor) throws FilterException {
		
		super(factor);
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {
		
		return (fileToCheack.length() <= this.FACTOR);
	}

}
