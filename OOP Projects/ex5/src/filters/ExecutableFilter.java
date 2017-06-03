package filters;

import java.io.File;

/**
 * Filter of files that are executable or not.
 * 
 * @author YONI
 *
 */
class ExecutableFilter extends YesOrNoFilter {
	/** Filter Name */
	static final String NAME_FILTER = "executable";
	
	/**
	 * Constructor.
	 * 
	 * @param yesOrNoExecutable - "YES" or "NO" some functionality.
	 * @throws FilterException  - if some other string yesOrNoFunction then the "YES" or "NO".
	 */
	public ExecutableFilter(String yesOrNoExecutable) throws FilterException {

		super(yesOrNoExecutable);
	}

	@Override
	public boolean filterDirectory(File fileToCheack) {
		
		return (fileToCheack.canExecute() == this.YES_OR_NO_FUNCTIONALITY);
	}

}
