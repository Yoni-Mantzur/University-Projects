package ex3;

/**
 * A super class for hash sets, implementing SimpleSet interface.
 * 
 * @see SimpleSet
 * @author YONI
 *
 */
public abstract class SimpleHashSet implements SimpleSet{
	
	/* The default  initializing upper load factor for the hashSet */
	private static final float DEFAULT_UPPER_LOAD_FACTOR = 0.75f;
	
	/* The default  initializing lower load factor for the hashSet */
	private static final float DEFAULT_LOWER_LOAD_FACTOR = 0.25F; 
	
	/* The default  initializing size table for the hashSet */
	private static final int DEFAULT_INITIALIZE_SIZE_TABLE = 16;
	
	private static int MIN_TABLE_SIZE = 1;
	
	// The values will not change!
	private final float  upperLoadFactor, lowerLoadFactor;
	
	private float loadFactor;
	
	// The current of items in the table.
	private int occupancyTable;
	
	
	/**
	 * Constructor.
	 */
	protected SimpleHashSet(){
		
		this(DEFAULT_UPPER_LOAD_FACTOR, DEFAULT_LOWER_LOAD_FACTOR);
	}
	
	
	/**
	 * Constructor.
	 * @param - upperLoadFactor - the upper limit of loading.
	 * @param - lowerLoadFactor - the lower limit of loading. 
	 */
	protected SimpleHashSet(float upperLoadFactor, float lowerLoadFactor){
		
		this.initializeHashTable(DEFAULT_INITIALIZE_SIZE_TABLE);
		this.upperLoadFactor = upperLoadFactor;
		this.lowerLoadFactor = lowerLoadFactor;
		this.loadFactor = 0f;
		this.occupancyTable = 0;
	}
	
	/**
	 * Constructor.
	 * 
	 * @param data - list of Strings wants to add to the set.
	 */
	protected SimpleHashSet(String[] data){
		
		this(DEFAULT_UPPER_LOAD_FACTOR, DEFAULT_LOWER_LOAD_FACTOR);
		
		for (String item : data)
			this.add(item);
		
		
	}
	
	/**
	 * Abstract function that charge on initializing the table.
	 * 
	 * @param capacity - the size of the table ( Default 16).
	 */
	protected abstract void initializeHashTable(int capacity);
		
	
	/**
	 * Check if the HashTable need to rehash.
	 * 
	 * @param reHashStatus - tells if the table is in rehash state.
	 * @param goalCapacity - means the number of the capacity after rehash (depends if add or deleted item).
	 * @return true if need to rehash or false other wise.
	 */
	protected boolean isReHashNeed(int goalCapacity, boolean reHashStatus){
		
		int capacity = this.capacity();
	
		// Check if the load factor tells rehash.
		if (!reHashStatus && (this.loadFactor > this.upperLoadFactor) && (goalCapacity > capacity)){
			
			this.occupancyTable = 0;
			return true;
			
		/* The minimal size of the table is the Default value */
		} else if (!reHashStatus && this.loadFactor < this.lowerLoadFactor && 
				(capacity >= MIN_TABLE_SIZE) && (goalCapacity < capacity)){
			
			this.occupancyTable = 0;
			return true;
		}
		return false;
	}
	
	/*
	 * Update the load factor.
	 */
	private void updateLoadFactor(int capacity, int size){
		
		this.loadFactor = (this.occupancyTable/(float)capacity);
	}
	

	
	/**
	 * Calculate the hashNumber regard to the table size.
	 * @param item - the String want to hash.
	 * @return the hashNumber of item.
	 */
	protected int getHashNumber(String item){
		return item.hashCode()&(this.capacity() - 1);
	}
		
	@Override
	public boolean add(String newValue) {
	
		if (newValue == null || this.contains(newValue)) //Check if already in the table.
			return false;

		this.occupancyTable++;
		updateLoadFactor(this.capacity(),this.occupancyTable);
		return true;
	}
	
	@Override
	public boolean delete(String toDelete){
			
		if (toDelete == null || !this.contains(toDelete))
			return false;

		this.occupancyTable--;
		updateLoadFactor(this.capacity(),this.occupancyTable);
		return true;
		
	}
	
	@Override
	public int size() {
		
		return this.occupancyTable;
	}
	

	/**
 	* @return - The current capacity (number of cells) of the table.  
 	*/
	public abstract int capacity(); 
}
