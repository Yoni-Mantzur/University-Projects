package filters;

import java.io.File;

/**
 * Filter of files that contains part of given string.
 * 
 * @author YONI
 *
 */
class EqualsNameFilter extends FileNameFilter {

	/** Filter Name */
	static final String NAME_FILTER = "file";
	
	/**
	 * Constructor.
	 * 
	 * @param name - same name of a file name. 
	 * @throws FilterException  - if the String is null.
	 */
	public EqualsNameFilter(String name) throws FilterException {

		super(name);
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {

		return (fileToCheack.getName().equals(this.COMPOSING_NAME));
		
	}

}
