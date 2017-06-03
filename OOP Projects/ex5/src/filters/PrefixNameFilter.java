package filters;

import java.io.File;

/**
 * Filter of files that have prefix of given string.
 * 
 * @author YONI
 *
 */
class PrefixNameFilter extends FileNameFilter {
	/** Filter Name */
	static final String NAME_FILTER = "perfix";
	
	/**
	 * Constructor.
	 * 
	 * @param prefix - prefix of a file name. 
	 * @throws FilterException - if the string is null.
	 */
	public PrefixNameFilter(String prefix) throws FilterException {

		super(prefix);
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {

		return (fileToCheack.getName().startsWith(this.COMPOSING_NAME));
	}

}
