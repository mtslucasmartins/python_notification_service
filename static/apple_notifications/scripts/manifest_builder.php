<?php

// This script creates a valid push package.
// This script assumes that the website.json file and iconset already exist. 
// This script creates a manifest and signature, zips the folder, and returns the push package. 

// Use this script as an example to generate a push package dynamically.

$package_version = 2;               // Change this to the desired push package version.

$certificate_path = "cert.p12";     // Change this to the path where your certificate is located
$certificate_password = ""; // Change this to the certificate's import password

// Convenience function that returns an array of raw files needed to construct the package.
function raw_files() {
    return array(
        'icon.iconset/icon_16x16.png',
        'icon.iconset/icon_16x16@2x.png',
        'icon.iconset/icon_32x32.png',
        'icon.iconset/icon_32x32@2x.png',
        'icon.iconset/icon_128x128.png',
        'icon.iconset/icon_128x128@2x.png',
        'website.json'
    );
}

// Creates the manifest by calculating the hashes for all of the raw files in the package.
function create_manifest($package_dir, $package_version) {

    // Obtain hashes of all the files in the push package
    $manifest_data = array();
    foreach (raw_files() as $raw_file) {
        $file_contents = file_get_contents("$package_dir/$raw_file");
        if ($package_version === 1) {
            $manifest_data[$raw_file] = sha1($file_contents);
        } else if ($package_version === 2) {
            $hashType = 'sha512';
            $manifest_data[$raw_file] = array(
                'hashType' => $hashType,
                'hashValue' => hash($hashType, $file_contents),
            );
        } else {
            throw new Exception('Invalid push package version.');
      }
    }
    file_put_contents("$package_dir/manifest.json", json_encode((object)$manifest_data));
}

// Zips the directory structure into a push package, and returns the path to the archive.
function package_raw_data($package_dir) {
    $zip_path = "$package_dir.zip";

    // Package files as a zip file
    $zip = new ZipArchive();
    if (!$zip->open("$package_dir.zip", ZIPARCHIVE::CREATE)) {
        error_log('Could not create ' . $zip_path);
        return;
    }

    $raw_files = raw_files();
    $raw_files[] = 'manifest.json';
    $raw_files[] = 'signature';
    foreach ($raw_files as $raw_file) {
        $zip->addFile("$package_dir/$raw_file", $raw_file);
    }

    $zip->close();
    return $zip_path;
}

// Creates the push package, and returns the path to the archive.
function create_push_package() {
    global $certificate_path, $certificate_password, $package_version;

    echo "\n\n\n\n\create_push_package\n\n\n\n";

    // Create a temporary directory in which to assemble the push package
    $package_dir = '/tmp/pushPackage' . time();
    if (!mkdir($package_dir)) {
        unlink($package_dir);
        echo "dying..";
        die;
    }

    echo "\n\n\n\n\created tmp\n\n\n\n";


    copy_raw_push_package_files($package_dir);
    echo "\n > copy_raw_push_package_files\n\n\n\n";


    create_manifest($package_dir, $package_version);
    echo "\n > create_manifest\n\n\n\n";


    create_signature($package_dir, $certificate_path, $certificate_password);
    echo "\n > create_signature\n\n\n\n";


    $package_path = package_raw_data($package_dir);
    echo "\n > package_raw_data\n\n\n\n";

    return $package_path;
}


// MAIN
// $package_path = create_push_package();

// create_signature("pushPackage.raw", "cert.p12", "");

create_manifest("pushPackage.raw", $package_version);

die;
