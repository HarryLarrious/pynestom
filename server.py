import socket
import struct
import threading
import uuid

from src.constants import *
from src.nbt import *
from src.packet.handler import *
from src.peer import Packet, Peer, State

# ====================================== CONSTANTS ======================================

# VERSION = "26.2"
# PROTOCOL = 776
# NAMESPACE = uuid.UUID("a9cfe996-7fe7-4bd1-aa58-96298f401e62")

# PACKETID_C2S_HANDSHAKE_INTENTION = 0x00

# PACKETID_C2S_STATUS_REQUEST = 0x00
# PACKETID_C2S_STATUS_PING = 0x01

# PACKETID_C2S_LOGIN_START = 0x00
# PACKETID_C2S_LOGIN_FINISH_ACKNOWLEDGE = 0x03

# PACKETID_C2S_CONFIG_CLIENT_INFO = 0x00
# PACKETID_C2S_CONFIG_CUSTOM_PAYLOAD = 0x02
# PACKETID_C2S_CONFIG_FINISH_ACKNOWLEDGE = 0x03
# PACKETID_C2S_CONFIG_KEEP_ALIVE = 0x04
# PACKETID_C2S_CONFIG_KNOWN_PACKS = 0x07

# PACKETID_C2S_PLAY_CONFIRM_TP = 0x00

# PACKETID_S2C_STATUS_RESPONSE = 0x00
# PACKETID_S2C_STATUS_PONG = 0x01

# PACKETID_S2C_LOGIN_FINISH = 0x02

# PACKETID_S2C_CONFIG_FINISH = 0x03
# PACKETID_S2C_CONFIG_REGISTRY_DATA = 0x07
# PACKETID_S2C_CONFIG_KNOWN_PACKS = 0x0E

# PACKETID_S2C_PLAY_ADD_ENTITY = 0x01
# PACKETID_S2C_PLAY_GAME_EVENT = 0x22
# PACKETID_S2C_PLAY_LOGIN = 0x2B
# PACKETID_S2C_PLAY_PLAYER_POS = 0x41
# PACKETID_S2C_PLAY_RESPAWN = 0x4B


# ====================================== GLOBALS ======================================

next_network_entity_id: int = 0

# ====================================== PACKET HANDLING ======================================


# def handle_handshake(peer: Peer):
#     packet_len = peer.read_varint()
#     packet_id = peer.read(1)[0]

#     if packet_id != PACKETID_C2S_HANDSHAKE_INTENTION:
#         raise Exception(f"Expected handshake packet (0x00), got {hex(packet_id)}")

#     protocol_version = peer.read_varint()
#     server_addr = peer.read_str()
#     server_port = struct.unpack(">H", peer.read(2))[0]
#     intention = peer.read_varint()

#     print(
#         f"Handshake - Protocol: {protocol_version}, Address: {server_addr}, Port: {server_port}, Intention: {intention}"
#     )

#     if intention == 1:
#         peer.state = State.STATUS
#     elif intention == 2 or intention == 3:
#         peer.state = State.LOGIN
#     else:
#         raise ConnectionError(f"unknown intention `{hex(intention)}`")
#     print(f"state = {peer.state}")


# def handle_status(peer: Peer):
#     packet_len = peer.read_varint()
#     print("len", packet_len)
#     packet_id = peer.read(1)[0]
#     print("recv", hex(packet_id))

#     if packet_id == PACKETID_C2S_STATUS_REQUEST:
#         status_json = (
#             '{"version":{"name":"'
#             + VERSION
#             + '","protocol":'
#             + str(PROTOCOL)
#             + '},"description":{"text":"I HATE MC PROTOCOL!!!!!!!"}}'
#         )
#         peer.send(Packet(PACKETID_S2C_STATUS_RESPONSE).write_str(status_json))

#     elif packet_id == PACKETID_C2S_STATUS_PING:
#         ping_id = peer.read(8)
#         peer.send(Packet(PACKETID_S2C_STATUS_PONG).write(ping_id))

#     else:
#         raise ConnectionError(f"unknown status packet, got {hex(packet_id)}")


# def handle_login(peer: Peer):
#     global next_network_entity_id

#     packet_len = peer.read_varint()
#     packet_id = peer.sock.recv(1)[0]

#     if packet_id == PACKETID_C2S_LOGIN_START:
#         peer.username = peer.read_str()
#         peer.sent_uuid = peer.sock.recv(16)
#         peer.uuid = uuid.uuid3(NAMESPACE, peer.username).bytes

#         print(f"Login start - Username: {peer.username}")

#         peer.send(
#             Packet(PACKETID_S2C_LOGIN_FINISH)
#             .write(peer.uuid)
#             .write_str(peer.username)
#             .write_varint(0)
#         )

#     elif packet_id == PACKETID_C2S_LOGIN_FINISH_ACKNOWLEDGE:
#         peer.state = State.CONFIGURATION
#         print("STATE_CONFIGURATION")

#         peer.send(
#             Packet(PACKETID_S2C_CONFIG_KNOWN_PACKS)
#             .write(struct.pack("B", 1))
#             .write_str("minecraft")
#             .write_str("core")
#             .write_str(VERSION)
#         )

#         for simple_registry in ["cat", "chicken", "cow", "frog", "pig"]:
#             peer.send(
#                 Packet(PACKETID_S2C_CONFIG_REGISTRY_DATA)
#                 .write_str(f"minecraft:{simple_registry}_variant")
#                 .write_varint(1)
#                 .write_str("minecraft:empty")
#                 .write(True)
#                 .write_nbt(
#                     NbtCompound(
#                         {
#                             "asset_id": NbtString("minecraft:empty"),
#                         }
#                     )
#                 )
#             )

#         damage_types = [
#             "fireworks",
#             "trident",
#             "hot_floor",
#             "sting",
#             "indirect_magic",
#             "stalagmite",
#             "mob_attack_no_aggro",
#             "outside_border",
#             "unattributed_fireball",
#             "magic",
#             "in_wall",
#             "dragon_breath",
#             "generic_kill",
#             "fly_into_wall",
#             "wind_charge",
#             "freeze",
#             "falling_anvil",
#             "fall",
#             "out_of_world",
#             "player_attack",
#             "starve",
#             "in_fire",
#             "arrow",
#             "dry_out",
#             "generic",
#             "thorns",
#             "explosion",
#             "wither_skull",
#             "mob_attack",
#             "mob_projectile",
#             "fireball",
#             "mace_smash",
#             "player_explosion",
#             "spit",
#             "on_fire",
#             "cactus",
#             "wither",
#             "thrown",
#             "drown",
#             "sonic_boom",
#             "lava",
#             "cramming",
#             "lightning_bolt",
#             "sweet_berry_bush",
#             "falling_stalectite",
#             "ender_pearl",
#             "campfire",
#             "falling_block",
#             "bad_respawn_point",
#         ]
#         damage_type_packet: Packet = (
#             Packet(PACKETID_S2C_CONFIG_REGISTRY_DATA)
#             .write_str("minecraft:damage_type")
#             .write_varint(len(damage_types))
#         )
#         for damage_type in damage_types:
#             (
#                 damage_type_packet.write_str(f"minecraft:{damage_type}")
#                 .write(True)
#                 .write_nbt(
#                     NbtCompound(
#                         {
#                             "message_id": NbtString("empty"),
#                             "scaling": NbtString("never"),
#                             "exhaustion": NbtFloat(0.0),
#                         }
#                     )
#                 )
#             )

#         peer.send(
#             Packet(PACKETID_S2C_CONFIG_REGISTRY_DATA)
#             .write_str(f"minecraft:painting_variant")
#             .write_varint(1)
#             .write_str("minecraft:empty")
#             .write(True)
#             .write_nbt(
#                 NbtCompound(
#                     {
#                         "asset_id": NbtString("minecraft:empty"),
#                         "height": NbtInt(1),
#                         "width": NbtInt(1),
#                     }
#                 )
#             )
#         )
#         peer.send(
#             Packet(PACKETID_S2C_CONFIG_REGISTRY_DATA)
#             .write_str(f"minecraft:wolf_variant")
#             .write_varint(1)
#             .write_str("minecraft:empty")
#             .write(True)
#             .write_nbt(
#                 NbtCompound(
#                     {
#                         "assets": NbtCompound(
#                             {
#                                 "wild": NbtString("minecraft:empty"),
#                                 "tame": NbtString("minecraft:empty"),
#                                 "angry": NbtString("minecraft:empty"),
#                             }
#                         )
#                     }
#                 )
#             )
#         )
#         peer.send(
#             Packet(PACKETID_S2C_CONFIG_REGISTRY_DATA)
#             .write_str(f"minecraft:wolf_sound_variant")
#             .write_varint(1)
#             .write_str("minecraft:empty")
#             .write(True)
#             .write_nbt(
#                 NbtCompound(
#                     {
#                         "hurt_sound": NbtString("minecraft:empty"),
#                         "pant_sound": NbtString("minecraft:empty"),
#                         "whine_sound": NbtString("minecraft:empty"),
#                         "ambient_sound": NbtString("minecraft:empty"),
#                         "death_sound": NbtString("minecraft:empty"),
#                         "growl_sound": NbtString("minecraft:empty"),
#                     }
#                 )
#             )
#         )

#         peer.send(
#             Packet(PACKETID_S2C_CONFIG_REGISTRY_DATA)
#             .write_str(f"minecraft:worldgen/biome")
#             .write_varint(1)
#             .write_str("minecraft:plains")
#             .write(True)
#             .write_nbt(
#                 NbtCompound(
#                     {
#                         "has_precipitation": NbtByte(1),
#                         "temperature": NbtFloat(0.8),
#                         "downfall": NbtFloat(0.4),
#                         "effects": NbtCompound(
#                             {
#                                 "fog_color": NbtInt(12638463),
#                                 "water_color": NbtInt(4159204),
#                                 "water_fog_color": NbtInt(329011),
#                                 "sky_color": NbtInt(7907327),
#                             }
#                         ),
#                     }
#                 )
#             )
#         )
#         peer.send(
#             Packet(PACKETID_S2C_CONFIG_REGISTRY_DATA)
#             .write_str(f"minecraft:dimension_type")
#             .write_varint(1)
#             .write_str("minecraft:overworld")
#             .write(True)
#             .write_nbt(
#                 NbtCompound(
#                     {
#                         "has_skylight": NbtByte(0),
#                         "has_ceiling": NbtByte(0),
#                         "ultrawarm": NbtByte(0),
#                         "natural": NbtByte(1),
#                         "cordinate_scale": NbtDouble(1.0),
#                         "bed_works": NbtByte(1),
#                         "respawn_anchor_works": NbtByte(0),
#                         "min_y": NbtInt(0),
#                         "height": NbtInt(64),
#                         "logical_height": NbtInt(64),
#                         "infiniburn": NbtString("#minecraft:infiniburn_overworld"),
#                         "effects": NbtString("minecraft:overworld"),
#                         "ambient_light": NbtFloat(1.0),
#                         "piglin_safe": NbtByte(0),
#                         "has_raids": NbtByte(1),
#                         "monster_spawn_light_level": NbtCompound(
#                             {
#                                 "type": NbtString("minecraft:uniform"),
#                                 "min_inclusive": NbtInt(0),
#                                 "max_inclusive": NbtInt(0),
#                             }
#                         ),
#                         "monster_spawn_block_light_limit": NbtInt(0),
#                     }
#                 )
#             )
#         )

#         peer.send(Packet(PACKETID_S2C_CONFIG_FINISH))

#         network_entity_id = next_network_entity_id
#         next_network_entity_id += 1
#         spawn_dimension = "minecraft:overworld"
#         game_mode = 0
#         spawn_pos = [0.0, 1.0, 0.0]
#         peer.send(
#             Packet(PACKETID_S2C_PLAY_LOGIN)
#             .write(struct.pack(">i", network_entity_id))  # Network entity id
#             .write(False)  # Hardcore
#             .write_varint(1)
#             .write_str(spawn_dimension)
#             .write_varint(1)
#             .write_varint(4)  # View distance
#             .write_varint(4)  # Simulation distance
#             .write(False)  # Reduced debug info
#             .write(True)  # Show respawn screen on death
#             .write(True)  # Limited crafting
#             .write_varint(0)
#             .write_str(spawn_dimension)
#             .write(struct.pack(">l", 0))
#             .write(game_mode)
#             .write(struct.pack("b", -1))
#             .write(False)  # Is debug world
#             .write(True)  # Is superflat
#             .write(0)
#             .write_varint(0)
#             .write_varint(0)  # Sea level
#             .write(False)  # Enforces chat signatures
#         )
#         peer.send(
#             Packet(PACKETID_S2C_PLAY_ADD_ENTITY)
#             .write_varint(network_entity_id)
#             .write(peer.uuid)
#             .write_varint(149)  # Entity type
#             .write(struct.pack(">d", spawn_pos[0]))  # X
#             .write(struct.pack(">d", spawn_pos[1]))  # Y
#             .write(struct.pack(">d", spawn_pos[2]))  # Z
#             .write(struct.pack("B", 0))
#             .write(struct.pack("B", 0))
#             .write(struct.pack("B", 0))
#             .write_varint(0)
#             .write(struct.pack(">h", 0))
#             .write(struct.pack(">h", 0))
#             .write(struct.pack(">h", 0))
#         )
#         peer.send(
#             Packet(PACKETID_S2C_PLAY_RESPAWN)
#             .write_varint(0)
#             .write_str(spawn_dimension)
#             .write(struct.pack(">l", 0))
#             .write(game_mode)
#             .write(struct.pack("b", -1))
#             .write(False)  # Is debug world
#             .write(True)  # Is superflat
#             .write(0)
#             .write_varint(0)
#             .write_varint(0)  # Sea level
#             .write(0)
#         )
#         peer.send(
#             Packet(PACKETID_S2C_PLAY_GAME_EVENT).write(13).write(struct.pack(">f", 0.0))
#         )
#         peer.send(
#             Packet(PACKETID_S2C_PLAY_PLAYER_POS)
#             .write_varint(0)
#             .write(struct.pack(">d", spawn_pos[0]))  # X
#             .write(struct.pack(">d", spawn_pos[1]))  # Y
#             .write(struct.pack(">d", spawn_pos[2]))  # Z
#             .write(struct.pack(">h", 0))  # Velocity X
#             .write(struct.pack(">h", 0))  # Velocity Y
#             .write(struct.pack(">h", 0))  # Velocity Z
#             .write(struct.pack(">f", 0.0))  # Yaw
#             .write(struct.pack(">f", 0.0))  # Pitch
#         )

#     else:
#         raise ConnectionError(f"unknown login packet, got {hex(packet_id)}")


# def handle_config(peer: Peer):
#     packet_len = peer.read_varint()
#     packet_id = peer.sock.recv(1)[0]

#     if packet_id == PACKETID_C2S_CONFIG_CLIENT_INFO:
#         locale = peer.read_str()
#         view_distance = struct.unpack("b", peer.read(1))[0]
#         chat_mode = peer.read_varint()
#         chat_colors = struct.unpack("?", peer.read(1))[0]
#         skin_parts = struct.unpack("B", peer.read(1))[0]
#         main_hand = peer.read_varint()
#         text_filtering = struct.unpack("?", peer.read(1))[0]
#         allow_listing = struct.unpack("?", peer.read(1))[0]
#         particles = peer.read_varint()

#         print(f"Client Info - Locale: {locale}, View Distance: {view_distance}")

#     elif packet_id == PACKETID_C2S_CONFIG_CUSTOM_PAYLOAD:
#         peer.bytecount = 0
#         channel = peer.read_str()
#         data = peer.read(packet_len - peer.bytecount - 1)
#         print(f"Plugin Message - Channel: {channel}")

#     elif packet_id == PACKETID_C2S_CONFIG_FINISH_ACKNOWLEDGE:
#         peer.state = State.PLAY
#         print("STATE_PLAY")

#     elif packet_id == PACKETID_C2S_CONFIG_KEEP_ALIVE:
#         peer.read(8)
#         print("got keep alive")

#     elif packet_id == PACKETID_C2S_CONFIG_KNOWN_PACKS:
#         length = peer.read_varint()
#         for _ in range(length):
#             peer.read_str()
#             peer.read_str()
#             peer.read_str()
#         print("got known packs")

#     else:
#         raise Exception(f"Unknown config packet, got {packet_id}")


# def handle_play(client):
#     raise Exception("yippie!!!")


# ===================================================================================


def _handle_client(peer_sock: socket.socket, peer_addr: str):
    with peer_sock:
        print(f"New peer, {peer_addr}")
        peer = Peer(peer_sock, peer_addr)
        try:
            while True:
                if peer.state == State.HANDSHAKING:
                    handle_handshake(peer)
                elif peer.state == State.STATUS:
                    handle_status(peer)
                elif peer.state == State.LOGIN:
                    handle_login(peer)
                elif peer.state == State.CONFIGURATION:
                    handle_config(peer)
                elif peer.state == State.PLAY:
                    handle_play(peer)
        except ConnectionError:
            print(f"Peer {peer_addr} disconnected")


def server(host="0.0.0.0", port=25565):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen()

        print(f"Server listning on port {host}:{port}...")

        while True:
            peer_sock, peer_addr = server_sock.accept()
            peer_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            peer_thread = threading.Thread(
                target=_handle_client, args=(peer_sock, peer_addr)
            )
            peer_thread.start()


# ===================================================================================

if __name__ == "__main__":
    server()
