
/**
 * @title Flickr Crawler
 * @author R. Nazarbek
 * @since 16-5-2022
 * @version 1.1.0
 * This program is a web crawler for Flickr with a purpose of retrieving images from the website - 
 * for forensic/research purposes.
 */

package main;

import com.flickr4java.flickr.Flickr;
import com.flickr4java.flickr.photos.Photo;
import com.flickr4java.flickr.photos.PhotoList;
import com.flickr4java.flickr.REST;
import com.flickr4java.flickr.FlickrException;
import com.flickr4java.flickr.cameras.*;

import java.net.MalformedURLException;
import java.net.URISyntaxException;
import java.net.URL;
import java.awt.Desktop;
import java.awt.image.BufferedImage;

import com.drew.imaging.ImageMetadataReader;
import com.drew.imaging.ImageProcessingException;
import com.drew.imaging.jpeg.JpegMetadataReader;
import com.drew.imaging.jpeg.JpegProcessingException;
import com.drew.metadata.Directory;
import com.drew.metadata.Metadata;
import com.drew.metadata.Tag;
//import com.drew.metadata.exif.ExifDirectory;

import org.apache.commons.imaging.ImageReadException;
import org.apache.commons.imaging.Imaging;
import org.apache.commons.imaging.common.ImageMetadata;
import org.apache.commons.imaging.formats.tiff.datareaders.ImageDataReader;
import org.w3c.dom.*;

import java.io.*;
import java.util.*;
import javax.imageio.*;
import javax.imageio.stream.*;
import javax.imageio.metadata.*;

import com.groupdocs.metadata.core.*;

//Joptionpane imports

import javax.swing.*;


public class FlickrCrawler {

	/**
	 * All existing cameras (models)
	 */
	private static List<Camera> allCameras = new ArrayList<Camera>();

	/**
	 * 
	 */
	private static List<String> dupCams = new ArrayList<String>();
	/**
	 * All existing brands
	 */
	private static List<Brand> allBrands = new ArrayList<Brand>();

	/**
	 * All retrieved photos
	 */
	private static List<Photo> allPhotos = new ArrayList<Photo>();

	/**
	 * Count of all existing brands
	 */
	private static int totalBrands = allBrands.size();

	/**
	 * Count of all existing cameras (models)
	 */
	private static int totalCameras = allCameras.size();

	/**
	 * Flickr API key
	 * TODO enter API Key
	 */
	private static String apikey = "";

	/**
	 * Flickr Secret key
	 * TODO enter secret
	 */
	private static String secret = "";

	/**
	 * Flickr object
	 */
	private static Flickr flickr = new Flickr(apikey, secret, new REST());

	//private static Desktop desktop = java.awt.Desktop.getDesktop();
	
	private static String saveLocation;

	public static void main(String[] args) {
		
		
		allBrands.clear();
		allCameras.clear();
		allPhotos.clear();
		
		
		
		JTextField ApiKey = new JTextField();
		JTextField Secret = new JTextField();
		JTextField imagesPerCamera = new JTextField();
				
		Object[] fields = {
				"Api Key", ApiKey,
				"Secret", Secret,
				"Images Per Camera", imagesPerCamera
		};
		
		JOptionPane.showConfirmDialog(null, fields, "Enter values", JOptionPane.OK_CANCEL_OPTION
				, JOptionPane.INFORMATION_MESSAGE);

		apikey = ApiKey.getText();
		secret = Secret.getText();
		int requestedPhotos = Integer.parseInt(imagesPerCamera.getText());
		
		JFileChooser chooseSaveLocation = new JFileChooser();
		File currentDir = new File("Desktop");
		chooseSaveLocation.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
		
		File nameDir, namePath;
		
		chooseSaveLocation.setCurrentDirectory(currentDir);
		int check = chooseSaveLocation.showOpenDialog(null);
		
		System.out.println(ApiKey);
		System.out.println(secret);
		System.out.println(requestedPhotos);
		
		if (check == JFileChooser.APPROVE_OPTION) {
			nameDir = chooseSaveLocation.getCurrentDirectory();
			namePath = chooseSaveLocation.getSelectedFile();
			System.out.println("Dir: " + nameDir.getName());
			System.out.println("Path: " + namePath.getAbsolutePath());
			
			
			//Return all brands and cams
			try {
				getBrands();
				System.out.println("All brands captured...");
			} catch (FlickrException e1) {
				// TODO Auto-generated catch block
				// e1.printStackTrace();
			}
			
			//Get all models
			try {
				getModels();
				System.out.println("All cameras captured...");
			} catch (FlickrException e1) {
				// TODO Auto-generated catch block
				//e1.printStackTrace();
			}
			
			//Get all images
			
			try {
				getImage();
			} catch (FlickrException e) {
				// TODO Auto-generated catch block
				//e.printStackTrace();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (ImageProcessingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			/*
			try {
				downloadImages(namePath.getAbsolutePath());
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			*/

			
		} else {
			JOptionPane.showMessageDialog(null, "Process Aborted", "Cancel Dialog Box", JOptionPane.WARNING_MESSAGE);
		}

		
//		System.out.println("All images retrieved...");
//		System.out.println(allPhotos.size() + " photos retrieved.");
		

	}
	
	/**
	 * Returns a list of all brands
	 * 
	 * @return list of brands
	 * @throws FlickrException
	 */
	public static void getBrands() throws FlickrException {

		allBrands.addAll(flickr.getCamerasInterface().getBrands());
		System.out.println("Brands size: " + allBrands.size());
		for (Brand b : allBrands) {
			System.out.println(b.getName());
		}

	}

	/**
	 * Get all the models of each brand
	 * 
	 * @param b
	 * @return list of models
	 * @throws FlickrException
	 */
	public static void getModels() throws FlickrException {

		for (Brand b : allBrands) {

			try {
				allCameras.addAll(flickr.getCamerasInterface().getBrandModels(b.getName()));
			} catch (FlickrException e) {
				//allCameras.add(null);
			}
			
			

			// System.out.print(allCameras.size());
		}
		System.out.println("Cameras size: " + allCameras.size());
		for (Camera c: allCameras) {
			//System.out.println(c.getName());
			System.out.println(c.getName());
		}
		
	}

	/**
	 * Print all models and brands
	 */
	public static void printAll() {

		System.out.println("\n\nLoading...");

		System.out.println("The total number of camera brands: " + totalBrands);
		System.out.println("The total number of camera models: " + totalCameras);

		System.out.printf("\n\nAll brands (%d): \n\n", totalBrands);

		int newLine = 0;

		for (Brand b : allBrands) {
			System.out.printf("%-30.30s", b.getName());
			newLine++;

			if (newLine % 5 == 0) {
				System.out.println("");
			}
		}

		System.out.printf("\n\nAll models (%d): \n\n", totalCameras);

		int newLine2 = 0;

		for (Camera c : allCameras) {
			System.out.printf("%-35.35s", c.getName());
			newLine2++;
			if (newLine2 % 5 == 0) {
				System.out.println("");
			}
		}
	}

	/**
	 * Download specified number of images.
	 * Dont use this, use Selenium instead!!
	 * 
	 * @throws IOException
	 */
	public static void downloadImages(String folderName) throws IOException {

		for (Photo p : allPhotos) {

			URL url;
			try {

				url = new URL(p.getOriginalUrl());
				
				File t = new File(folderName + "/" + p.getId() + ".JPG");
				
				InputStream is = url.openStream();
				OutputStream os = new FileOutputStream(t);
				
				byte[] b = new byte[2048];
				int length;
				
				while ((length = is.read(b)) != -1) {
					os.write(b, 0, length);
				}
				
				is.close();
				os.close();
								
			} catch (MalformedURLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (FlickrException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

	/**
	 * Write all brands and models to TXT file.
	 * 
	 * @throws IOException
	 */
	public static void writeToFile() throws IOException {

		BufferedWriter br = new BufferedWriter(new FileWriter("data.txt"));

		br.write("The total number of camera brands: " + totalBrands);
		br.write("The total number of camera models: " + totalCameras);

		br.write(String.format("\n\nAll brands (%d): \n\n", totalBrands));

		int newLine = 0;

		for (Brand b : allBrands) {
			br.write(String.format("%-30.30s", b.getName()));
			newLine++;

			if (newLine % 5 == 0) {
				br.write("");
			}
		}

		br.write(String.format("\n\nAll models (%d): \n\n", totalCameras));

		int newLine2 = 0;

		for (Camera c : allCameras) {
			br.write(String.format("%-35.35s", c.getName()));
			newLine2++;
			if (newLine2 % 5 == 0) {
				br.write("");
			}
		}
		br.close();
	}

	
	/**
	 * Return image specific to camera
	 * Don't use this, use Selenium instead!!
	 * 
	 * @param camera
	 * @param amount
	 * @throws FlickrException
	 * @throws InterruptedException 
	 * @throws IOException 
	 * @throws ImageProcessingException 
	 */
	public static void getImage() throws FlickrException, InterruptedException, ImageProcessingException, IOException {

		Set<String> b = new HashSet<String>();
		b.add("url_o");
		b.add("machine_tags");
		
		while (dupCams.size() < allCameras.size()) {
			PhotoList<Photo> photos = flickr.getPhotosInterface().getRecent(b, 100, 100);
			for (int i = 0; i < photos.size(); i++) {
				if (getModelName(photos.get(i)) != "Unidentified Model" && !dupCams.contains(getModelName(photos.get(i)))) {
					System.out.println(getModelName(photos.get(i)));
				}
				
				if (!dupCams.contains(getModelName(photos.get(i))) && getModelName(photos.get(i)) != "Unidentified Model") {
					dupCams.add(getModelName(photos.get(i)));
					allPhotos.add(photos.get(i));
					System.out.println(dupCams.size());
				}
			}
			photos = flickr.getPhotosInterface().getRecent(b, 100, 100);
		}
	}
	
	/**
	 * Return model of image
	 * 
	 * @param p
	 * @return
	 * @throws IOException
	 * @throws InterruptedException
	 * @throws ImageProcessingException
	 */
	public static String getModelName(Photo p) throws IOException, InterruptedException, ImageProcessingException {
		
		URL url;
		String model = "Unidentified Model";

		try {

			url = new URL(p.getOriginalUrl());
			
			File temp = new File("tempFile.JPG");
			
			InputStream is = url.openStream();
			OutputStream os = new FileOutputStream(temp);
			
			byte[] b = new byte[2048];
			int length;
			
			while ((length = is.read(b)) != -1) {
				os.write(b, 0, length);
			}
			
			is.close();
			os.close();
			
			Metadata m = ImageMetadataReader.readMetadata(temp);
			
			for (Directory d : m.getDirectories()) {
				for (Tag t: d.getTags()) {
					for (Tag s: d.getTags()) {
						if (s.getTagName().equals("Make")) {
							if (t.getTagName().equals("Model")) {
								if (t.getDescription() != null
									&& s.getDescription() != null) {
									model = "";
									model += s.getDescription();
									model += " ";
									model += t.getDescription();
								}
							}
						}
					}
				}
			}
			
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			//e.printStackTrace();
		} catch (FlickrException e) {
			// TODO Auto-generated catch block
			//e.printStackTrace();
		}

		return model;	
	}
}
