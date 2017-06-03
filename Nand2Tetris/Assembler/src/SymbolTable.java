import java.util.Hashtable;

/**
 * Facade that charge on symbol table.
 * @author Yoni
 *
 */
public class SymbolTable 
{
	// Capcity of the initialized table. 
	private static final int INIT_CAPACITY = 30;
	
	// The symbol table
	private Hashtable<String, Integer> symbolTable;
	
	/*
	 * Constructor
	 */
	public SymbolTable()
	{
		this.symbolTable = new Hashtable<>(INIT_CAPACITY);
	}
	
	/**
	 * Add an entry to the symbol table.
	 * @param symbol - the symbol of the address
	 * @param address - the address to add.
	 */
	public void addEntry(String symbol, int address)
	{
		this.symbolTable.put(symbol, address);
	}
	
	/**
	 * Check if the given symbol is contained in the symbol table.
	 * @param symbol
	 * @return true if it is in table.
	 */
	public boolean isContains(String symbol)
	{
		return this.symbolTable.containsKey(symbol);
	}
	
	/**
	 * @param symbol
	 * @return the address of the given  symbol.
	 * @exception - if the symbol doesn't exists return null
	 */
	public int getAddress(String symbol)
	{
		return this.symbolTable.get(symbol);		
	}
	
	public int size()
	{
		return symbolTable.size();
	}
	

}
