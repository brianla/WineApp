package csv;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;

public class CSVRow implements Serializable{
	
	/*
	 * Description:
	 * 
	 * 		-Represents a single row from the Angkor Export CSV
	 * 		-Contains various data pertaining to a single publication
	 */
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 626057866300589220L;
	/*
	 * Vars
	 */
	//Pre-Process Variables
	private ArrayList<String> rowAsArray = new ArrayList<String>();
	private CSVHeaderRow thisHeader;
	private Boolean debugMode;
	private ArrayList<String> rowData;
	
	//Post-Process Variables
	private HashMap<String, String> mappedValues = new HashMap<String, String>();
	
	public CSVRow()
	{
		this(false);
	}
	
	public CSVRow(CSVHeaderRow header)
	{
		this(false);
		thisHeader = header;
	}
	
	public CSVRow(Boolean debug)
	{
		debugMode = debug;
	}
	
	public CSVRow(CSVHeaderRow header, ArrayList<String> rowData)
	{
		this(header, rowData, false);
	}
	
	public CSVRow(CSVHeaderRow header, ArrayList<String> rowData, Boolean debug)
	{
		thisHeader = header;
		debugMode = debug;
		this.rowData = rowData;
		process(rowData);
	}
	
	public void remapHeader()
	{
		mapValuesToHeader(thisHeader, rowAsArray);
	}
	
	public void remapHeader(CSVHeaderRow header)
	{
		thisHeader = header;
		mapValuesToHeader(thisHeader, rowAsArray);
	}
	
	private void process(ArrayList<String> rowData)
	{
		mapValuesToHeader(thisHeader, rowData);
	}
	
	private String removeQuotes(String str)
	{
		String cell = new String(str);
		if(cell.length() > 2)
		{
			if(cell.charAt(0) == '\'' || cell.charAt(0) == '"')
				cell = cell.substring(1, cell.length());
			if(cell.charAt(cell.length()-1) == '\'' || cell.charAt(cell.length()-1) == '"')
				cell = cell.substring(0, cell.length()-1);
		}else{
			Boolean pass = true;
			for(int i = 0; i < cell.length(); i++)
				if(!(cell.charAt(i) == '\'' || cell.charAt(i) == '"'))
					pass = false;
			if(pass)
				cell = new String("");
		}
		return cell;
	}
	
	private void mapValuesToHeader(CSVHeaderRow header, ArrayList<String> values)
	{
		mappedValues = new HashMap<String, String>();
		if(header.getValues().size() == values.size()+1)
			values.add(" ");//If the row's last cell is blank Scythe will drop the cell, this fixes it
			
		if(header.getValues().size() == values.size())
		{
			String noQuoteValue;
			for(int i = 0; i < header.getValues().size(); i++)
			{
				noQuoteValue = removeQuotes(values.get(i));
				mappedValues.put(header.getValues().get(i), noQuoteValue);
			}
		}else{
			if(debugMode)
				loadingError(header, values);
		}
	}

	private void loadingError(CSVHeaderRow header, ArrayList<String> values)
	{
		System.err.println("CSVRow:  Header provided does not match the Row provided.  Header[" + header.getValues().size() + "] =!= Row[" + values.size() + "]");

		System.err.print("Header:  ");
		for(int i = 0; i < header.getValues().size(); i++)
		{
			if(i != 0)
				System.err.print(", ");
			System.err.print(header.getValues().get(i));
		}
		System.err.print("\nRow:  ");
		for(int i = 0; i < values.size(); i++)
		{
			if(i != 0)
				System.err.print(", ");
			System.err.print(values.get(i));
		}
		System.err.println("");
		
		for(int i = 0; i < values.size() || i < header.getValues().size(); i++)
		{
			if(i < header.getValues().size())
				System.out.print("Header:  " + header.getValues().get(i) + "\t");
			else
				System.out.print("Header:  " + "-----" + "\t");
			if(i < values.size())
				System.out.println("Value:  " + values.get(i));
			else
				System.out.println("Value:  " + "-----");
		}
	}
	
	public String getValueByKey(String key) 
	{
		String val = mappedValues.get(thisHeader.transform(key));
		if(val == null)
			val = mappedValues.get(key);
		return val;
	}
	
	public void setMappedValues(HashMap<String, String> mappedValues)
	{
		this.mappedValues = mappedValues;
	}
	
	public void putMappedPair(String key, String value)
	{
		String tKey = thisHeader.transform(key);
		if(!thisHeader.getValues().contains(tKey))
			System.err.println("CSVRow:  Error:  Current Key [" + tKey + "] does not exist in the header row.  This cell will be lost upon saving to file.");
		mappedValues.put(thisHeader.transform(key), value);
	}
	
	public void setHeaderRow(CSVHeaderRow headerRow)
	{
		thisHeader = headerRow;
	}
	
	public String getFormattedRow()
	{
		String fRow = new String("");
		for(int i = 0; i < thisHeader.getValues().size(); i++)
		{
			if(i != 0)
				fRow += ",";
			fRow += "\"";
			
			if(mappedValues.get(thisHeader.getValues().get(i)) == null)
				fRow += "";
			else
				fRow += mappedValues.get(thisHeader.getValues().get(i)).replaceAll("\"", "'");
			
			fRow += "\"";
		}
		return fRow;
	}
	
	public CSVHeaderRow getHeader()
	{
		return thisHeader;
	}
	
	public ArrayList<String> getArr()
	{
		return rowData;
	}
	
	public ArrayList<String> makeArr()
	{
		ArrayList<String> arr = new ArrayList<String>();
		for(int i = 0; i < thisHeader.getValues().size(); i++) {
			String val = mappedValues.get(thisHeader.getValues().get(i));
			if(val != null)
				arr.add(val);
			else
				arr.add("");
		}
		return arr;
	}
	
	public HashMap<String, String> getMappedValues()
	{
		return mappedValues;
	}
}
