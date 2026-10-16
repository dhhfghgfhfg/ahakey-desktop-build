import SwiftUI

private struct LegacyGeometryPreference<Value: Equatable>: PreferenceKey {
    static var defaultValue: Value? { nil }

    static func reduce(value: inout Value?, nextValue: () -> Value?) {
        if let next = nextValue() { value = next }
    }
}

private struct CompatibilityGeometryObserver<Value: Equatable>: ViewModifier {
    let transform: (GeometryProxy) -> Value
    let action: (Value) -> Void

    @ViewBuilder
    func body(content: Content) -> some View {
        if #available(macOS 13.0, *) {
            content.onGeometryChange(for: Value.self, of: transform, action: action)
        } else {
            content.background {
                GeometryReader { proxy in
                    Color.clear.preference(key: LegacyGeometryPreference<Value>.self, value: transform(proxy))
                }
            }
            .onPreferenceChange(LegacyGeometryPreference<Value>.self) { value in
                if let value { action(value) }
            }
        }
    }
}

extension View {
    func onCompatGeometryChange<Value: Equatable>(
        for type: Value.Type,
        of transform: @escaping (GeometryProxy) -> Value,
        action: @escaping (Value) -> Void
    ) -> some View {
        modifier(CompatibilityGeometryObserver(transform: transform, action: action))
    }
}
