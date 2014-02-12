package csv;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;

import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JOptionPane;

import csv.au.com.bytecode.opencsv.CSVReader;

import backend.ApplicationVariables;

import file.SimpleFileFilter;
import file.SimplePrinter;


public class CSV implements Serializable{
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 8158070492860343536L;
	/*
	 * Vars
	 */
	private Boolean loaded = false;
	private Boolean debugMode = false;
	private String directory = new String("");
	private File thisFile = null;
	
	private CSVHeaderRow headerRow = new CSVHeaderRow();
	private ArrayList<CSVRow> rows = new ArrayList<CSVRow>();
	
	private Transform headerTransform;
	
	
	public CSV()
	{
		this(false);
	}
	
	public CSV(Transform trans)
	{
		this(false);
		headerTransform = trans;
	}
	
	public CSV(Boolean debug)
	{
		debugMode = debug;
	}
	
	public CSV(File csv)
	{
		this(csv, false);	
	}
	
	public CSV (File csv, Transform trans)
	{
		headerTransform = trans;
		thisFile = csv;
		debugMode = false;
	    directory = csv.getParentFile().getPath() + "\\";
		process(thisFile);
	}
	
	public CSV(File csv, Boolean debug)
	{
		thisFile = csv;
		debugMode = debug;
	    directory = csv.getParentFile().getPath() + "\\";
		process(thisFile);
	}
	
	public Boolean loadCSVSpreadsheet(File csv)
	{
		if(loaded)
			return false;

		thisFile = csv;
		process(thisFile);
		return true;
	}
	
	public void openFileChooser()
	{
		thisFile = openFileChooserDialog();
		if(thisFile == null){
			loaded = false;
		}else{
			process(thisFile);
			loaded = true;
		}
	}
	
	private File openFileChooserDialog()
	{
		System.out.println("Opening CSV");		
	    JFileChooser chooser = new JFileChooser((String)ApplicationVariables.vars.get(ApplicationVariables.Constants.lastUserOpenLocation));
	    chooser.addChoosableFileFilter(new SimpleFileFilter(".csv"));
	    chooser.setDialogTitle("Select a valid CSV file (eg: mySpreadSheet.csv)");
	    chooser.setApproveButtonToolTipText("Select CSV");	    
	    int choice = chooser.showDialog((new JFrame()), "Select CSV");
	    if (choice != JFileChooser.APPROVE_OPTION) {
	      return null;
	    }	    
	    File file = chooser.getSelectedFile();
	    if(file == null)
	    	return null;
	    
	    ApplicationVariables.vars.put(ApplicationVariables.Constants.lastUserOpenLocation, file.getParentFile());	
	    
	    if ( !file.exists() ){
	      return null;
	    }
	    if ( file.exists() && !file.canRead() ){
	      return null;
	    }	
			
	    directory = file.getParentFile().getPath() + "\\";
	    
	    return file;
	}
	
	private void process(File file)
	{
		Boolean headerFlag = false;
		ArrayList<ArrayList<String>> csvRows = generateRows(file);
		rows = new ArrayList<CSVRow>();
		for(int i = 0; i < csvRows.size(); i++)
		{
			if(csvRows.get(i) != null)
			{
				if(!headerFlag)
				{
					headerRow = new CSVHeaderRow(csvRows.get(i), headerTransform);
					headerFlag = true;
				}else
					rows.add(new CSVRow(headerRow, csvRows.get(i), debugMode));
			}
		}
		System.err.println("Loaded " + rows.size() + " rows from CSV Spreadsheet");
	}
	
	private ArrayList<ArrayList<String>> generateRows(File file)
	{
		ArrayList<ArrayList<String>> rowList = new ArrayList<ArrayList<String>>();
		String[] nextLine;
		try {
			CSVReader reader = new CSVReader(new FileReader(file));
			while ((nextLine = reader.readNext()) != null) 
			{
				ArrayList<String> rowValues = new ArrayList<String>();
		        for(int i = 0; i < nextLine.length; i++)
		        	rowValues.add(nextLine[i]);
		        rowList.add(rowValues);
		    }
		} catch (FileNotFoundException e) {
			System.err.println("CSV:  generateRows():  ERROR:  File not found.");
			e.printStackTrace();
		} catch (IOException e) {
			System.err.println("CSV:  generateRows():  ERROR:  File read error.");
			e.printStackTrace();
		}		
		return rowList ;
	}
	
	public CSVColumn getColumn(String key)
	{
		if(headerRow.getValues().contains(key))
		{
			ArrayList<String> items = new ArrayList<String>();
			for(int i = 0; i < rows.size(); i++)
				items.add(rows.get(i).getValueByKey(key));
			return new CSVColumn(key, items);
		}
		
		System.err.println("ERROR:  CSV:  getCloumn():  The key provided is not a valid key for this CSV (" + thisFile.getName() + ").");
		return null;		
	}
	/**
	 * Adds a column to the end of the table, or overwrites an existing column with the same header —v’ˆÓII
	 * @param col
	 */
	public void addColumn(CSVColumn col)
	{
		if(!headerRow.getValues().contains(col.key))
			headerRow.getValues().add(col.key);
		for(int i = 0; i < rows.size() || i < col.items.size(); i++)
		{
			if(i < rows.size() && i < col.items.size())
			{
				rows.get(i).setHeaderRow(headerRow);	
				rows.get(i).putMappedPair(col.key, col.items.get(i));
			}else if (i < rows.size()){
				rows.get(i).setHeaderRow(headerRow);
				rows.get(i).putMappedPair(col.key, "");
			}else{
				rows.add(new CSVRow(headerRow));
				rows.get(i).putMappedPair(col.key, col.items.get(i));
			}
		}
	}
	
	public boolean changeColumnHeader(String oldHeader, String newHeader)
	{
		int loc = -1;
		for(int i = 0; i < headerRow.getValues().size(); i++){
			String val = headerRow.getValues().get(i);
			if(val.equals(oldHeader)){
				loc = i;
				System.out.println("Converting HeaderRow from [" + oldHeader + "] to [" + newHeader +"]");
				headerRow.getValues().set(i, newHeader);
				break;
			}
		}
		if(loc <= -1)
			return false;
		for(int i = 0; i < rows.size(); i++){
			CSVRow row = rows.get(i);
			row.putMappedPair(newHeader, row.getValueByKey(oldHeader));
		}
		return true;
	}
	
	public File saveAs()
	{
		return saveAs(null);
	}
	
	public File saveAs(String path)
	{
		File file = null;
		if(path == null)
		{
			System.out.println("Saving CSV to File:");		
		    JFileChooser chooser = new JFileChooser((String)ApplicationVariables.vars.get(ApplicationVariables.Constants.lastUserSaveLocation));
		    chooser.addChoosableFileFilter(new SimpleFileFilter(".csv"));
		    chooser.setDialogTitle("Saving CSV to File (eg: myFile.csv)");
		    chooser.setApproveButtonToolTipText("Save");	    
		    int choice = chooser.showDialog((new JFrame()), "Save");
		    if (choice != JFileChooser.APPROVE_OPTION) {
		      return null;
		    }	    
		    file = chooser.getSelectedFile();
		    ApplicationVariables.vars.put(ApplicationVariables.Constants.lastUserSaveLocation, file.getParentFile());
		}else{
			file = new File(path);
		}
		
	    if(file.exists())
	    {
	    	Integer verInt = JOptionPane.showConfirmDialog(new JFrame(), "File Exists:  Would you like to overwrite? (" + file.getPath() + ")");
		    if(verInt == 0)
		    {
				SimplePrinter sp = new SimplePrinter(file.getPath().endsWith(".csv") ? file.getPath() : file.getPath() + ".csv"/*.replaceAll(".csv", "") + ".csv"*/);
				printToFile(sp);
				sp.close();
				return new File(file.getPath().endsWith(".csv") ? file.getPath() : file.getPath() + ".csv");
		    }
		    return saveAs(null);
	    }
	    
	    SimplePrinter sp = new SimplePrinter(file.getPath().endsWith(".csv") ? file.getPath() : file.getPath() + ".csv"/*.replaceAll(".csv", "") + ".csv"*/);
	    printToFile(sp);
	    sp.close();
	    return new File(file.getPath().endsWith(".csv") ? file.getPath() : file.getPath() + ".csv");
	}
	
	public void filterAwayAllOfMikesWorries() throws Exception
	{
		//Worry #1:		", \r"
		for(int j = 0; j < headerRow.getValues().size(); j++)
		{
			String key = headerRow.getValues().get(j);
			for(int i = 0; i < rows.size(); i++)
				rows.get(i).putMappedPair(key, rows.get(i).getValueByKey(key).replace(", \r", "; "));
		}
	}
	
	public void filterOutOfRangeText() throws Exception
	{
		for(int j = 0; j < headerRow.getValues().size(); j++)
		{
			String key = headerRow.getValues().get(j);
			for(int i = 0; i < rows.size(); i++)
				rows.get(i).putMappedPair(key, filterText(rows.get(i).getValueByKey(key)));
		}
	}
	
	private String filterText(String t)
	{
		String valid = new String();
		for(int i = 0; i < t.length(); i++)
		{
			if(XMLChar.isValid(t.charAt(i)))
				valid += t.charAt(i);
			else
				System.err.println("CSV:  filterText():  Found Invalid Character (" + t.charAt(i) + ") in String (" + t + ")");
		}
		return valid;
	}
	
	public void printToFile(SimplePrinter sp)
	{
		sp.println(headerRow.getFormattedHeader());
		for(int i = 0; i < rows.size(); i++)
			sp.println(rows.get(i).getFormattedRow());
	}
	
	public void remapHeader()
	{
		for(int i = 0; i < rows.size(); i++)
			rows.get(i).remapHeader();
	}
	
	public boolean isLoaded()
	{
		return loaded;
	}

	public String getDirectory() 
	{
		return directory;
	}

	public void setDirectory(String directory) 
	{
		this.directory = directory;
	}

	public File getThisFile() 
	{
		return thisFile;
	}

	public void setThisFile(File thisFile) 
	{
		this.thisFile = thisFile;
	}
	
	public CSVHeaderRow getHeaderRow()
	{
		return headerRow;
	}
	
	public void setHeaderRow(CSVHeaderRow headerRow)
	{
		this.headerRow = headerRow;
	}

	public ArrayList<CSVRow> getRows() 
	{
		return rows;
	}

	public void setRows(ArrayList<CSVRow> rows) 
	{
		this.rows = rows;
	}

}
