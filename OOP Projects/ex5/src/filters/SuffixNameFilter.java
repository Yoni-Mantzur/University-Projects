package filters;

import java.io.File;

/**
 * Filter of files that have suffix of given string.
 * 
 * @author YONI
 *
 */
class SuffixNameFilter extends FileNameFilter {
	/** Filter Name */
	static final String NAME_FILTER = "suffix";
	
	/**
	 * Constructor.
	 * 
	 * @param suffix - suffix of a file name. 
	 * @throws FilterException - if the string is null.
	 */
	public SuffixNameFilter(String suffix) throws FilterException{
		
		super(suffix);
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {

		return (fileToCheack.getName().endsWith(this.COMPOSING_NAME));
	}

}
