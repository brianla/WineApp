package csv;

import java.io.Serializable;
import java.util.ArrayList;

public class CSVHeaderRow implements Serializable{
	
	/*
	 * Description:
	 * 
	 * 		-Represents a single row from a CSV
	 */
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -7204732963465595795L;

	/*
	 * Vars
	 */
	private ArrayList<String> values = new ArrayList<String>();
	private Transform t = new Transform();
	
	public CSVHeaderRow()
	{
		
	}
	
	public CSVHeaderRow(ArrayList<String> rowData)
	{
		process(rowData);
		//System.err.println("LOADTEST:  " + rowData.toString());
	}
	
	public CSVHeaderRow(ArrayList<String> rowData, Transform trans)
	{
		t = trans;
		process(rowData);
	}
	
	private void process(ArrayList<String> rowData)
	{
		values = new ArrayList<String>();
		for(int i = 0; i < rowData.size(); i++)
			values.add(removeQuotes(rowData.get(i)).replace("\r", "").replace("\n", "").trim());
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
	
	public String getFormattedHeader()
	{
		String fHead = new String("");
		for(int i = 0; i < values.size(); i++)
		{
			if(i != 0)
				fHead += ",";
			fHead += "\"";
			fHead += values.get(i).replaceAll("\"", "'");
			fHead += "\"";
		}
		return fHead;
	}

	public ArrayList<String> getValues() 
	{
		return values;
	}

	public void setValues(ArrayList<String> values) 
	{
		this.values = values;
	}
	
	public Transform getTransform()
	{
		return t;
	}
	
	public void addTransform(String input, String key)
	{
		t.addTransform(input, key);
	}
	
	public void removeTransform(String input)
	{
		t.removeTransform(input);
	}
	
	public String transform(String input)
	{
		if(t == null)
			t = new Transform();
		String rtn = t.transform(input);
		return (rtn == null || rtn.isEmpty()) ? input : rtn;
	}

}
