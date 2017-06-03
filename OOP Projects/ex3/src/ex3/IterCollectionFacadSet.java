package ex3;

import java.util.Collection;
import java.util.Iterator;

/**
 * Warps a Collection and serve basic api as extend CollectionFacadeSet
 * in addition to iteration ability, implementing Iterable<String>.
 * 
 * @See Iterable
 * @see CollectionFacadeSet
 * @author YONI
 *
 */
public class IterCollectionFacadSet extends CollectionFacadeSet implements
		 Iterable<String> {
	
	private Collection<String> collection;

	/**
	 * Constructor.
	 * @param collection - the collection to wrap
	 */
	public IterCollectionFacadSet(Collection<String> collection) {
		super(collection);
		this.collection = collection;
	}

	@Override
	public Iterator<String> iterator() {

		return this.collection.iterator();
	}


}
