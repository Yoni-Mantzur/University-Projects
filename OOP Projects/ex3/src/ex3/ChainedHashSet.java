package ex3;

import java.util.LinkedList;

/**
 * Hash set that composed from LinkLists.
 * 
 * @see SimpleHashSet
 * @author YONI
 *
 */
public class ChainedHashSet extends SimpleHashSet{
		
	private IterCollectionFacadSet[] hashTable;
	
	private boolean reHashStatus;
	private int capacityTable;
	
	/**
	 * Constructor.
	 */
	public ChainedHashSet() {
		
		super();		
		this.reHashStatus = false;
	}
	
	/**
	 * Constructor.
	 * 
	 * @param - upperLoadFactor - the upper limit of loading.
	 * @param - lowerLoadFactor - the lower limit of loading. 
	 */
	public ChainedHashSet(float upperLoadFactor, float lowerLoadFactor) {
		
		super(upperLoadFactor, lowerLoadFactor);
		this.reHashStatus = false;
	}
	
	/**
	 * Constructor.
	 * @param data - list of Strings wants to add to the set.
	 */
	public ChainedHashSet(String[] data){
	
		
		super(data);
		this.reHashStatus = false;
	}
	
	@Override
	/**
	 * Initialize the IterCollectionFacadSet Table.
	 * @param capacity - the new size of the table.
	 */
	protected void initializeHashTable(int capacity){
		
		this.capacityTable = capacity;
		this.hashTable =  new IterCollectionFacadSet[this.capacityTable];
		
	}


	@Override
	/**
	 * Check if need to rehash and done it case case. 
	 * @param  goalCapacity - the size of the table after rehash (means came from add or delete) 
	 * @param reHashStatus - tells if it call to rehash in current rehash.
	 * @return true if done rehash
	 */
	protected boolean isReHashNeed(int goalCapacity, boolean reHashStatus){
			
		if (super.isReHashNeed(goalCapacity, this.reHashStatus)){
			
			this.reHashStatus = true;
				
			// Resizing the table.
			IterCollectionFacadSet[] oldHashTable = this.hashTable;
			this.initializeHashTable(goalCapacity);
			
			for(int i=0; i<oldHashTable.length;i++){
				if (oldHashTable[i] == null)
					continue;
				
				for (String item : oldHashTable[i])	
					
					this.add(item);
			}
			this.reHashStatus = false;
			return true; // means rehash was done!
		}
		
		return false; // means rehash wasn't done!
	}

	@Override
	public boolean add(String newValue) {


		int hash_number = super.getHashNumber(newValue);

		if (!super.add(newValue))
			return false;
			
		// Initialize with linkList
		if (this.hashTable[hash_number] == null){
			this.hashTable[hash_number] = new IterCollectionFacadSet(new LinkedList<String>());
		}
				
		this.hashTable[hash_number].add(newValue);
		this.isReHashNeed(this.capacityTable *2, this.reHashStatus);
		return true;
	}


	@Override
	public boolean contains(String searchVal) {
		
		int hash_number = super.getHashNumber(searchVal); 
		return (this.hashTable[hash_number] != null) && (this.hashTable[hash_number].contains(searchVal));
	}


	@Override
	public boolean delete(String toDelete) {
		
		if (!super.delete(toDelete))
			return false;
			
		this.hashTable[super.getHashNumber(toDelete)].delete(toDelete);
		this.isReHashNeed(this.capacityTable /2, this.reHashStatus);
		return true;
		
	}
	
	@Override
	public int capacity() {
		// TODO Auto-generated method stub
		return this.hashTable.length;
	}
}
