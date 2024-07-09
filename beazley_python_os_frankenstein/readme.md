### Where does this monstrosity come from?

The purpose of this code is to study python generators/coroutines so I can implement Raft in a similar fashion to how resonate.io implemented their deterministic simulation.

[Reference for resonate DST](https://github.com/resonatehq/resonate/blob/main/test/dst/dst_test.go#L27)

[Reference for Beazley lecture (1h38ish)](https://www.youtube.com/watch?v=Z_OAlIhXziw&list=PLlwjO3dkXipTArHcbhD_ESp6bI8fVkGo-&index=16&ab_channel=DavidBeazley)

This should lay the foundation for an async io based network where raft peers and clients communicate and I can schedule everything deterministically. Let us see how it goes.