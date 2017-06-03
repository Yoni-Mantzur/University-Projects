package filters;

import java.io.File;

/**
 * Filter of files that are writable or not.
 * 
 * @author YONI
 *
 */
class WritableFilter extends YesOrNoFilter {
	/** Filter Name */
	static final String NAME_FILTER = "writable";
	
	/**
	 * Constructor.
	 * 
	 * @param yesOrNoWiritable - "YES" or "NO" some functionality.
	 * @throws FilterException  - if some other string yesOrNoFunction then the "YES" or "NO".
	 */
	public WritableFilter(String yesOrNoWiritable) throws FilterException {

		super(yesOrNoWiritable);
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {
	
		return (fileToCheack.canWrite() == this.YES_OR_NO_FUNCTIONALITY) ;
	}

}
