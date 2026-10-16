// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "VibeBar",
    platforms: [.macOS(.v12)],
    products: [
        .library(name: "VibeBar", targets: ["VibeBar"]),
        .executable(name: "VibeBarSmoke", targets: ["VibeBarSmoke"]),
    ],
    dependencies: [
        .package(path: "../vendor/DynamicNotchKit"),
    ],
    targets: [
        .target(
            name: "VibeBar",
            dependencies: [
                .product(name: "DynamicNotchKit", package: "DynamicNotchKit"),
            ],
            path: "Sources/VibeBar"
        ),
        .executableTarget(
            name: "VibeBarSmoke",
            dependencies: ["VibeBar"],
            path: "Sources/VibeBarSmoke"
        ),
        .testTarget(
            name: "VibeBarTests",
            dependencies: ["VibeBar"],
            path: "Tests/VibeBarTests"
        ),
    ]
)
