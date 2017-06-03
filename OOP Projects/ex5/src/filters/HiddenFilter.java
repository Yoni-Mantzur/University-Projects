package filters;

import java.io.File;

/**
 * Filter of files that are hidden or not.
 * 
 * @author YONI
 *
 */
class HiddenFilter extends YesOrNoFilter {

	/** Filter Name */
	static final String NAME_FILTER = "hidden";
	
	/**
	 * Constructor.
	 * 
	 * @param yesOrNoHidden - "YES" or "NO" some functionality.
	 * @throws FilterException  - if some other string yesOrNoFunction then the "YES" or "NO".
	 */
	public HiddenFilter(String yesOrNoHidden) throws FilterException {

		super(yesOrNoHidden);
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {
		
		return (fileToCheack.isHidden() == this.YES_OR_NO_FUNCTIONALITY);
	}

}
