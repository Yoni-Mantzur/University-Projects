package filters;

/**
 * Abstract Class representing Filter regarding exist character of the file, implementing Filter InterFace.
 * 
 * @author YONI
 * @see WritableFilter
 * @see ExecutableFilter
 * @see HiddenFilter
 */
abstract class YesOrNoFilter implements Filter{

	/* Represent with/without some character to filter*/
	private static final String WITH_FUNCTIONALTY = "YES", WITH_OUT_FUNCTIONALTY = "NO";
	
	/** Represent if there exist character of a file or not (true means exist). */
	protected final boolean YES_OR_NO_FUNCTIONALITY;	
			
	/**
	 * Constructor.
	 * 
	 * @param yesOrNoFunction - "YES" or "NO" some functionality.
	 * @throws FilterException  - if some other string yesOrNoFunction then the "YES" or "NO".
	 */
	public YesOrNoFilter(String yesOrNoFunction) throws FilterException{
		
		if (yesOrNoFunction.equals(WITH_FUNCTIONALTY))
			this.YES_OR_NO_FUNCTIONALITY = true;
		
		else if (yesOrNoFunction.equals(WITH_OUT_FUNCTIONALTY))
			this.YES_OR_NO_FUNCTIONALITY = false;
		
		else
			throw new FilterException();
		
	}

}
