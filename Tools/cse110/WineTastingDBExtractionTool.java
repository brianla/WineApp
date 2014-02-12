package cse110;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

import csv.CSV;
import csv.CSVHeaderRow;
import csv.CSVRow;

public class WineTastingDBExtractionTool implements Runnable {

	private final String dbFileName = "WineTastingDB.csv";
	private final String filterFileName = "WineTastingDB_FilterSheet.csv";
	private final String commonWordsFileName = "top250.txt";
	

	@Override
	public void run()
	{
		CSV db = loadDBintoCSV(dbFileName);
		HashSet<String> filterList = loadFilterList(filterFileName);
		ArrayList<String> commonWords = loadCommonWordList(commonWordsFileName);
		
		HashMap<String, Integer> wordCounts = extractWordCounts(db);
		
		CSV out = new CSV();
		ArrayList<String> header = new ArrayList<String>();
		header.add("Word");
		header.add("Count");
		header.add("Keep");
		header.add("Filter");
		CSVHeaderRow headRow = new CSVHeaderRow(header);
		out.setHeaderRow(headRow);
		
		ArrayList<CSVRow> rows = new ArrayList<CSVRow>();
		CSVRow row = null;
		for(Map.Entry<String, Integer> entry : wordCounts.entrySet())
		{
			if(isNumber(entry.getKey()) || entry.getValue() <= 1)
				continue;
			
			row = new CSVRow(headRow);
			row.putMappedPair(header.get(0), entry.getKey());
			row.putMappedPair(header.get(1), ""+entry.getValue());
			row.putMappedPair(header.get(2), "");
			row.putMappedPair(header.get(3), filterList.contains(entry.getKey()) ? "1" : "");
			
			rows.add(row);
		}
		out.setRows(rows);
		
		out.saveAs("WineTastingDB_WordCounts.csv");
		
		
		int count = 0;
		System.out.println(col("Word", 25) + col("Count", 25));
		for(Map.Entry<String, Integer> entry : wordCounts.entrySet())
		{
			if(isNumber(entry.getKey()) || entry.getValue() <= 1)
				continue;
			System.out.println(col(entry.getKey(), 25) + col(""+entry.getValue(), 25));
			++count;
		}
		System.out.println("Total Words: " + count);
	}
	
	private HashMap<String, Integer> extractWordCounts(CSV db)
	{
		HashMap<String, Integer> counts = new HashMap<String, Integer>();
		CSVRow row = null;
		String desc = null;
		ArrayList<String> tokens = null;
		String word = null;
		Integer count = 0;
		
		for(int i = 0; i < db.getRows().size(); i++)
		{
			row = db.getRows().get(i);
			desc = row.getValueByKey("Notes");
			tokens = tokenizeLine(desc);
			for(int j = 0; j < tokens.size(); j++)
			{
				word = tokens.get(j).toLowerCase();
				//if(filter.contains(word))
					//continue;
				count = counts.get(word);
				if(count == null)
					count = 0;
				counts.put(word, ++count);
			}
		}
		
		return counts;
	}
	
	
	
	
	
	
	
	
	
	
	private CSV loadDBintoCSV(String fileName)
	{
		CSV db = new CSV();
		db.loadCSVSpreadsheet(new File(fileName));
		return db;
	}
	
	private HashSet<String> loadFilterList(String fileName)
	{
		HashSet<String> filter = new HashSet<String>();
		CSV fcsv = new CSV();
		fcsv.loadCSVSpreadsheet(new File(fileName));
		
		CSVRow row = null;
		String filterFlag = null;
		for(int i = 0; i < fcsv.getRows().size(); i++)
		{
			row = fcsv.getRows().get(i);
			filterFlag = row.getValueByKey("Filter");
			if(filterFlag != null && !filterFlag.isEmpty())
			{
				filter.add(row.getValueByKey("Word"));
			}
		}
		
		return filter;
		
	}
	
	private ArrayList<String> loadCommonWordList(String fileName)
	{
		File datFile = new File(fileName);
		ArrayList<String> words = new ArrayList<String>();
		
		if(datFile == null|| !datFile.exists()) {
			System.err.println("\tException: File is null or does not exist.");
			return words;
		}
		
		if(datFile.exists())
		{
			ArrayList<String> lines = getLinesFromTextFile(datFile);
			for(int i = 0; i < lines.size(); i++) {
				words.add(lines.get(i).trim());
			}
		}else
			System.err.println("\tException: datFile at path " + datFile.getPath() + " does not exist.");
		
		return words;
	}
	
	private ArrayList<String> getLinesFromTextFile(File textFile)
	{
		ArrayList<String> lines = new ArrayList<String>();
		try {
			//Open the File as a buffered stream
			InputStream is = new FileInputStream(textFile);
			BufferedInputStream bis = new BufferedInputStream(is);
			
			String buffer = "";
			int c = 0;
			
			while((c = bis.read()) != -1)
			{
				if((char)c == '\n') {
					lines.add(buffer.trim());
					buffer = "";
				}else
					buffer += (char)c;
			}
			if(!buffer.trim().isEmpty())
				lines.add(buffer.trim());
			
			//Close the stream and release the lock on the file
			bis.close();
			
		} catch (Exception e) {
			System.err.println("\t" + e.getMessage());
		}
		return lines;
	}
	
	private ArrayList<String> tokenizeLine(String line)
	{
		ArrayList<String> tokens = new ArrayList<String>();
		String buf = "";
		char c = 0;
		int len = line.length();
		
		//Convert the line into a series of tokens delimited by white space
		for(int i = 0; i < len; i++)
		{
			c = line.charAt(i);
			if(isDelimiter(c)) {
				if(!buf.isEmpty()){
					tokens.add(buf);
					buf = "";
				}
			}else
				buf += c;
		}
		if(!buf.isEmpty())
			tokens.add(buf);
		return tokens;
	}
	
	private boolean isDelimiter(char c)
	{
		return Character.isWhitespace(c)
				|| c == ','	|| c == '<'
				|| c == '>'	|| c == '.'
				|| c == '/'	|| c == '?'
				|| c == ';'	|| c == ':'
				|| c == '\''|| c == '\"'
				|| c == '[' || c == '{'
				|| c == ']' || c == '}'
				|| c == '\\'|| c == '|'
				|| c == '-'	|| c == '_'
				|| c == '+'	|| c == '='
				|| c == '`'	|| c == '~'
				|| c == '!' || c == '@'
				|| c == '#'	|| c == '$'
				|| c == '%'	|| c == '^'
				|| c == '&'	|| c == '*'
				|| c == '('	|| c == ')';
	}
	
	private boolean isNumber(String str)
	{
		int len = str.length();
		for(int i = 0; i < len; i++)
			if(!Character.isDigit(str.charAt(i)))
				return false;
		return true;
	}
	
	private String col(String str, int width)
	{
		String fixedStr;
		if(str.length() > width) {
			fixedStr = str.substring(0, width);
		}else{
			int diff = width-str.length();
			fixedStr = new String(str);
			for(int i = 0; i < diff; i++)
				fixedStr += " ";
		}
		return fixedStr;
	}
	
	public static void main(String[] args)
	{
		WineTastingDBExtractionTool tool = new WineTastingDBExtractionTool();
		tool.run();
	}
}
