package filters;

import java.io.File;

class SmallerThanFilter extends SizeFilter {
	/** Filter Name */
	static final String NAME_FILTER = "smaller_than";
	
	
	/**
	 * Constructor.
	 * 
	 * @param factor - the factor of the size filter.
	 * @throws FilterException - if the factor not only numbers or negative.
	 */
	public SmallerThanFilter(String factor) throws FilterException{
		
		super(factor);
		
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {

		return (fileToCheack.length() >= this.FACTOR);
	}

}
