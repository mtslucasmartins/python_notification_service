<?php

// This script creates a valid push package.
// This script assumes that the website.json file and iconset already exist. 
// This script creates a manifest and signature, zips the folder, and returns the push package. 

// Use this script as an example to generate a push package dynamically.

$package_version = 2;               // Change this to the desired push package version.

$certificate_path = "cert.p12";     // Change this to the path where your certificate is located
$certificate_password = ""; // Change this to the certificate's import password

// Creates a signature of the manifest using the push notification certificate.
function create_signature($package_dir, $cert_path, $cert_password) {
    // Load the push notification certificate
    $pkcs12 = file_get_contents($cert_path);
    $certs = array();
    if(!openssl_pkcs12_read($pkcs12, $certs, $cert_password)) {
        return;
    }

    $signature_path = "$package_dir/signature";

    // Sign the manifest.json file with the private key from the certificate
    $cert_data = openssl_x509_read($certs['cert']);
    $private_key = openssl_pkey_get_private($certs['pkey'], $cert_password);
    openssl_pkcs7_sign("$package_dir/manifest.json", $signature_path, $cert_data, $private_key, array(), PKCS7_BINARY | PKCS7_DETACHED);

    // Convert the signature from PEM to DER
    $signature_pem = file_get_contents($signature_path);
    $matches = array();
    if (!preg_match('~Content-Disposition:[^\n]+\s*?([A-Za-z0-9+=/\r\n]+)\s*?-----~', $signature_pem, $matches)) {
        return;
    }
    $signature_der = base64_decode($matches[1]);
    file_put_contents($signature_path, $signature_der);
}


// MAIN
create_signature("pushPackage.raw", "cert.p12", "");
die;
