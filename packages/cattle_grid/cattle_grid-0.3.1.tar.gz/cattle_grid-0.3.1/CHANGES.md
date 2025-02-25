# Changes

## 0.3.1 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10557))

- Repair reload for extensions run [cattle_grid#105](https://codeberg.org/bovine/cattle_grid/issues/105)

## 0.3.0 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10442))

- Add a simple method rewriting [cattle_grid#101](https://codeberg.org/bovine/cattle_grid/issues/101)
- Enable configuring fakeredis as the key value database [cattle_grid#104](https://codeberg.org/bovine/cattle_grid/issues/104)
- Improved reported [cattle_grid#14](https://codeberg.org/bovine/cattle_grid/issues/14)
- Add a run command for extensions [cattle_grid#99](https://codeberg.org/bovine/cattle_grid/issues/99)
- remove cattle_grid.config.messaging [cattle_grid#100](https://codeberg.org/bovine/cattle_grid/issues/100)
- testing.fixtures now contains an sqlalchemy engine [cattle_grid#96](https://codeberg.org/bovine/cattle_grid/issues/96)
- Add client.gen to generate ts docs [cattle_grid#97](https://codeberg.org/bovine/cattle_grid/issues/97)

## 0.2.8 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10324))

- Add command `account delete NAME` [cattle_grid#92](https://codeberg.org/bovine/cattle_grid/issues/92)
- Add command to prune deleted actors [cattle_grid#40](https://codeberg.org/bovine/cattle_grid/issues/40)
- Separated create and add identifier [cattle_grid#62](https://codeberg.org/bovine/cattle_grid/issues/62)
- Make more dependency injections generally available [cattle_grid#94](https://codeberg.org/bovine/cattle_grid/issues/94)
- Add missing docker tags to build step [cattle_grid#93](https://codeberg.org/bovine/cattle_grid/issues/93)
- Add a simple register extension [cattle_grid#52](https://codeberg.org/bovine/cattle_grid/issues/52)
- Update actor.profile instead of overwriting it [cattle_grid#91](https://codeberg.org/bovine/cattle_grid/issues/91)
- Improve documentation of TypeScript SDK [cattle_grid#89](https://codeberg.org/bovine/cattle_grid/issues/89)
- Add management of PropertyValue for actor [cattle_grid#57](https://codeberg.org/bovine/cattle_grid/issues/57)

## 0.2.7 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9769))

- Manually cancel FastAPI streams
- Add heartbeat to streaming [cattle_grid#88](https://codeberg.org/bovine/cattle_grid/issues/88)
- Add action to rename actors [cattle_grid#87](https://codeberg.org/bovine/cattle_grid/issues/87)
- Cleanup amqp queues
- Mark actors as deleted instead of deleting [cattle_grid#85](https://codeberg.org/bovine/cattle_grid/issues/85)
- Allow naming actors in the account [cattle_grid#76](https://codeberg.org/bovine/cattle_grid/issues/76)
- Include body in release
- Repair shared inbox [cattle_grid#84](https://codeberg.org/bovine/cattle_grid/issues/84)

## 0.2.6 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9700))

- Adjust trigger interface to match async api [cattle_grid#80](https://codeberg.org/bovine/cattle_grid/issues/80)
- Use node info object [cattle_grid#81](https://codeberg.org/bovine/cattle_grid/issues/81)
- Implement sharedInbox [cattle_grid#78](https://codeberg.org/bovine/cattle_grid/issues/78)

## 0.2.5 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9680))

- Added account name to InformationResponse [cattle_grid#77](https://codeberg.org/bovine/cattle_grid/issues/77)
- Check if public identifiers exist when creating actor [cattle_grid#75](https://codeberg.org/bovine/cattle_grid/issues/75)
- Repair streaming endpoints [cattle_grid#79](https://codeberg.org/bovine/cattle_grid/issues/79)
- Improve generate javascript package [cattle_grid#74](https://codeberg.org/bovine/cattle_grid/issues/74)

## 0.2.4 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9659))

- Document how to use cattle_grid.auth with caddy [cattle_grid#43](https://codeberg.org/bovine/cattle_grid/issues/43)
- More fine grained control of logging
- `/account/stream/type` now properly handles type [cattle_grid#68](https://codeberg.org/bovine/cattle_grid/issues/68)
- Start updating Account API to match Cattle Drive and start building typescript SDK [cattle_grid#67](https://codeberg.org/bovine/cattle_grid/issues/67)

## 0.2.3 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9654))

- Add basic permission structure for accounts [cattle_grid#47](https://codeberg.org/bovine/cattle_grid/issues/47)
- Handle another Undo Follow case [cattle_grid#60](https://codeberg.org/bovine/cattle_grid/issues/60)
- Add verified public identifiers [cattle_grid#50](https://codeberg.org/bovine/cattle_grid/issues/50)

## 0.2.2 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9648))

- Add configuration flag `processor_in_app` [cattle_grid#54](https://codeberg.org/bovine/cattle_grid/issues/54)
- Actors are now removed from account on delete [cattle_grid#56](https://codeberg.org/bovine/cattle_grid/issues/56)
- Remove `cattle_grid.exchange.server`, [cattle_grid#55](https://codeberg.org/bovine/cattle_grid/issues/55)

## 0.2.1 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9647))

- Enable building docker containers in CI [cattle_grid#49](https://codeberg.org/bovine/cattle_grid/issues/49)
- Implement `X-Cattle-Grid-Should-Serve` header [Issue#10](https://codeberg.org/bovine/cattle_grid/issues/10)
- Better naming of exchanges [cattle_grid#46](https://codeberg.org/bovine/cattle_grid/issues/46)
- Forbid certain account names [cattle_grid#45](https://codeberg.org/bovine/cattle_grid/issues/45)
