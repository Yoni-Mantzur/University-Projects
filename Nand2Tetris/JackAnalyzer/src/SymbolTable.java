import java.util.Hashtable;

public class SymbolTable 
{
	
	public static enum Kind{
		STATIC,
		FIELD,
		ARG,
		VAR,
		NONE;
		
		public static Kind getTypeByName(String kind){
			if (kind.equals("static"))
				return STATIC;
			
			else if (kind.equals("field"))
				return FIELD;

			if (kind.equals("argument"))
				return ARG;
			
			else if (kind.equals("var"))
				return VAR;
			
			else 
				return NONE;
		}	
		
		public String toString()
		{
			switch(this){
				case STATIC: return "static";
				case FIELD: return "field";
				case ARG: return "argument";
				case VAR: return "var";
				default: return "none";
			}
		}
	}
	

	private static class Identifier
	{

		private Kind kind;
		private String type;
		private int runningIndex;
		
		public Identifier(String type, Kind kind, int runningIndex) {
			super();
			this.type = type;
			this.kind = kind;
			this.runningIndex = runningIndex;
		}		
		
		public String getType() {
			return type;
		}

		public Kind getKind() {
			return kind;
		}

		public int getRunningIndex() {
			return runningIndex;
		}
	}
	
	
	
	private Hashtable<Kind, Integer> countIndices;
	private Hashtable<String, Identifier> classScope;
	private Hashtable<String, Identifier> subrutineScope;	
	
	
	
	public SymbolTable()
	{
		this.countIndices = initalCountIndices();
		this.classScope = new Hashtable<>();
		this.subrutineScope = new Hashtable<>();		
	}
	
	private Hashtable<Kind, Integer> initalCountIndices()
	{
		 Hashtable<Kind, Integer> initalCountIndices = new Hashtable<>(4);
		 initalCountIndices.put(Kind.STATIC, 0);
		 initalCountIndices.put(Kind.FIELD, 0);
		 initalCountIndices.put(Kind.ARG, 0);
		 initalCountIndices.put(Kind.VAR, 0);
		 
		 return initalCountIndices;
	}
	
	public void startSubroutine()
	{
		subrutineScope.clear();
		countIndices.put(Kind.ARG, 0);
		countIndices.put(Kind.VAR, 0);
	}
	
	public void define(String name, String type, Kind kind)
	{
		if (kind == Kind.NONE)
			return;
		
		int index = this.countIndices.get(kind);
		Identifier newIdentifier = new Identifier(type, kind, index);
		
		if (kind == Kind.STATIC || kind == Kind.FIELD)
			this.classScope.put(name, newIdentifier);
		
		else
			this.subrutineScope.put(name, newIdentifier);
		
		this.countIndices.put(kind, index+1);
		

//		System.out.println("new define: type : " + type.toString() +" name : " + name + " kind : " + kind + " index : " + index);
//		System.out.println("number indices of kind : " + kind.toString() + " is : " + varCount(kind));
	}
	
	public int varCount(Kind kind)
	{
		return this.countIndices.get(kind);
	}
	
	public Kind kindOf(String name)
	{
		Identifier ident = this.getIdentifierByName(name);
		
		if (ident == null)
			return Kind.NONE;
		return ident.getKind();
	}
	
	public String typedOf(String name)
	{
		Identifier ident = this.getIdentifierByName(name);
		
		if (ident == null)
			return null;
		
		return ident.getType();
	}
	
	public int indexOf(String name)
	{
		Identifier ident = this.getIdentifierByName(name);
		
		if (ident == null)
			return -1;
		
		return ident.getRunningIndex();
	}
	
	public Identifier getIdentifierByName(String name)
	{
		Identifier ident = this.subrutineScope.get(name);
		
		if (ident == null)
			ident = this.classScope.get(name);
		
		return ident;
	}

}
