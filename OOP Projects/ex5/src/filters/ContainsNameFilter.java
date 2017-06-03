package filters;

import java.io.File;

/**
 * Filter of files that contains part of given string.
 * 
 * @author YONI
 *
 */
class ContainsNameFilter extends FileNameFilter {

	/** Filter Name */
	static final String NAME_FILTER = "file";
	
	/**
	 * Constructor.
	 * 
	 * @param composingName - part of a file name. 
	 * @throws FilterException  - if the string is null.
	 */
	public ContainsNameFilter(String composingName) throws FilterException {

		super(composingName);
	}

	
	@Override
	public boolean filterDirectory(File fileToCheack) {
		
		return (fileToCheack.getName().contains(this.COMPOSING_NAME));
	}

}
