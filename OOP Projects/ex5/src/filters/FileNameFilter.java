package filters;

/**
 * Abstract Class representing Filter regarding a name of the file, implementing Filter InterFace.
 * 
 * @author YONI
 * @see EqualsNameFilter
 * @see ContainsNameFilter
 * @see SuffixFilter
 * @see PrefixFiltter
 */
abstract class FileNameFilter implements Filter{

	/** Represent part of a name of file  */
	protected final String COMPOSING_NAME;	
	
	/**
	 * Constructor.
	 * 
	 * @param composingName - part (or same) of a file name. 
	 * @throws FilterException - if the string is null.
	 */
	public FileNameFilter(String composingName) throws FilterException {
		
		if (composingName == null)
			throw new FilterException();
		
		this.COMPOSING_NAME = composingName;
	}

}
