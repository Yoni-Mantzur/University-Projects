package ex3;

import java.util.Collection;

/**
 * Warps a Collection and serve basic Api, implementing SimpleSet.
 * 
 * @See SimpleSet
 * @author YONI
 *
 */
public class CollectionFacadeSet implements SimpleSet {
	
	private Collection<java.lang.String> collection;
	
	/**
	 * Constructor.
	 * @param collection - the collection to wrap.
	 */
	public CollectionFacadeSet(Collection<java.lang.String> collection) {
		
		this.collection = collection;
	}
	

	 
	@Override
	public boolean add(String newValue) {
		
			return this.collection.add(newValue);
	}

	@Override
	public boolean contains(String searchVal) {

		return this.collection.contains(searchVal);
	}

	@Override
	public boolean delete(String toDelete) {

		return this.collection.remove(toDelete);
	}

	@Override
	public int size() {

		return this.collection.size();
	}

}
