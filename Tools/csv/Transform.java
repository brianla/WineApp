package csv;

import java.util.LinkedHashMap;

public class Transform {
	
	/*
	 * This system will need to be re-thought and re-designed (
	 * 
	 * A simple class that acts as a translation layer between an input and the class that receives that input
	 * Ex:  Used to access the columns of a CSV sheet using values different than those values that are actually on that sheet.
	 */
	
	/*
	 * Vars
	 */
	private LinkedHashMap<String, String> trans;
	
	public Transform()
	{
		trans = new LinkedHashMap<String, String>();
	}
	
	public void addTransform(String input, String output)
	{
		trans.put(input, output);
	}
	
	public void removeTransform(String input)
	{
		trans.remove(input);
	}
	
	public String transform(String input)
	{
		String result = trans.get(input);
		if(result == null)
			return input;
		return result;
	}

}
