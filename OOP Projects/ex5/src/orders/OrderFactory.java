package orders;

/**
 * Factory of Order.
 *  
 * @author YONI
 *
 */
public class OrderFactory {
	
	/**
	 * Default order creation.
	 * @return the default order.
	 */
	public static Order createOrder(){
		
		return AbsOrder.instanceAbsOrder();		
	}

	
	/**
	 * Static method, return the order creation regard to the order name was given.
	 * 
	 * @param orderName - the name of the order to create.
	 * @param isReverse - the parameter.
	 * @throws OrderException - if the name of the order illegal or parameters.
	 * @return the order to create.
	 */
	public static Order createOrder(String orderName, String isReverse) throws OrderException{
		
		Order requiredOrder = null;
							
		if (orderName.equals(AbsOrder.ORDER_NAME))
			requiredOrder =  AbsOrder.instanceAbsOrder();
		
		else if (orderName.equals(SizeOrder.ORDER_NAME))
			requiredOrder =  SizeOrder.instanceSizeOrder();
		
		else if(orderName.equals(TypeOrder.ORDER_NAME))
			requiredOrder =  TypeOrder.instanceSizeOrder();
			
		// Parameter of revers.
		if (isReverse == ReverseOrder.ORDER_NAME)
			return new ReverseOrder(requiredOrder);
		
		else if (isReverse == null && requiredOrder != null)
			return requiredOrder;			
	
		
		// Means the name with error
		throw new OrderException();
		
	}

}
