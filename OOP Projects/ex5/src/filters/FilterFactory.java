package filters;


/**
 * Factory of filter.
 * 
 * @author YONI
 *
 */
public class FilterFactory {
	

	/**
	 * Default creatFilter.
	 * 
	 * @return the default filter.
	 */
	public static Filter createFilter(){
		
		return new AllFilesFilter(); 
	}
	
	/**
	 * Static method, return the filter creation regard to the filter name was given.
	 * 
	 * @param filterParameters - the name of the filter to create with it's parameters.
	 * @throws Exception  - if error with names filters or parameters.
	 */
	public static Filter createFilter (String nameFilter, String[] filterParameters,
																String isNegative) throws FilterException {
			Filter requiredFilter = null;
			String factor1 = filterParameters[0], factor2 = (filterParameters.length>1) ? 
																			filterParameters[1] : null;
			
			if (nameFilter.equals(GreaterThanFilter.NAME_FILTER))
				requiredFilter = new GreaterThanFilter(factor1);
		
			else if (nameFilter.equals(BetweenFilter.NAME_FILTER))
				requiredFilter = new BetweenFilter(factor1,factor2);
		
			else if (nameFilter.equals(SmallerThanFilter.NAME_FILTER))
				requiredFilter = new SmallerThanFilter(factor1);
		
			else if (nameFilter.equals(EqualsNameFilter.NAME_FILTER))	
				requiredFilter = new EqualsNameFilter(factor1);
		
			else if (nameFilter.equals(ContainsNameFilter.NAME_FILTER))	
				requiredFilter = new ContainsNameFilter(factor1);
		
			else if (nameFilter.equals(PrefixNameFilter.NAME_FILTER))
				requiredFilter = new PrefixNameFilter(factor1);
		
			else if (nameFilter.equals(SuffixNameFilter.NAME_FILTER))
				requiredFilter =  new SuffixNameFilter(factor1);
		
			else if (nameFilter.equals(WritableFilter.NAME_FILTER))
				requiredFilter = new WritableFilter(factor1);
		
			else if (nameFilter.equals(ExecutableFilter.NAME_FILTER))
				requiredFilter =  new ExecutableFilter(factor1);
		
			else if (nameFilter.equals(HiddenFilter.NAME_FILTER))
				requiredFilter =  new HiddenFilter(factor1);
		
			else if (nameFilter.equals(ExecutableFilter.NAME_FILTER))
				requiredFilter =  new ExecutableFilter(factor1);
		
			else if (nameFilter.equals(AllFilesFilter.NAME_FILTER))
				requiredFilter =  new AllFilesFilter();
						
			if (isNegative == NegativeFilter.NAME_FILTER)
				return new NegativeFilter(requiredFilter);

			else if (requiredFilter != null)
				return requiredFilter;
			
			// Means illegal name of filter or negative parameter.
			throw new FilterException();
	}
}
